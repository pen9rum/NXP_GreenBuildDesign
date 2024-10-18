#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <curl/curl.h>
#include "board.h"
#include "fsl_debug_console.h"
#include "gpio.h"
#include "cJSON.h"

// Firestore 設定
#define FIRESTORE_PROJECT_ID "greendesign-9ed49"
#define FIRESTORE_COLLECTION "your-collection"
#define ACCESS_TOKEN "AIzaSyC_MhhUwX49wqfPLJV7mhcEM0M_1l_zO7M" // 建議動態獲取

// 假設有這些函式的實現
void AM2120_StartSignal(void);
uint8_t AM2120_ReadBit(void);

// 函式聲明
void AM2120_ReadData(uint16_t *humidity, int16_t *temperature);
int upload_to_firestore(uint16_t humidity, int16_t temperature);

// 讀取 AM2120 數據
void AM2120_ReadData(uint16_t *humidity, int16_t *temperature) {
    uint8_t data[5] = {0};
    AM2120_StartSignal(); // 發送開始信號

    // 讀取 40 位資料 (5 bytes)
    for (int i = 0; i < 40; i++) {
        data[i / 8] <<= 1;
        data[i / 8] |= AM2120_ReadBit();
    }

    // 解析資料
    *humidity = (data[0] << 8) | data[1];        // 濕度完整數值（高位 + 低位）
    *temperature = (data[2] << 8) | data[3];     // 溫度完整數值（高位 + 低位）

    // 溫度可能是有符號的，因此轉換為 int16_t
    if (*temperature & 0x8000) { // 如果溫度為負
        *temperature = -((~(*temperature) + 1) & 0xFFFF);
    }

    // 簡單檢查校驗和
    uint8_t checksum = data[0] + data[1] + data[2] + data[3];
    if (checksum != data[4]) {
        PRINTF("Check sum error: humidity=%d, temperature=%d, checksum=%d\r\n", *humidity, *temperature, data[4]);
    }
}

// 上傳數據到 Firestore
int upload_to_firestore(uint16_t humidity, int16_t temperature) {
    CURL *curl;
    CURLcode res;
    int ret = 0;

    // 構建 Firestore URL
    char url[256];
    snprintf(url, sizeof(url),
             "https://firestore.googleapis.com/v1/projects/%s/databases/(default)/documents/%s",
             FIRESTORE_PROJECT_ID, FIRESTORE_COLLECTION);

    // 使用 cJSON 構建 JSON 數據
    cJSON *root = cJSON_CreateObject();
    cJSON *fields = cJSON_CreateObject();
    cJSON_AddItemToObject(root, "fields", fields);

    // 構建 humidity 字段
    cJSON *humidity_field = cJSON_CreateObject();
    cJSON_AddNumberToObject(humidity_field, "doubleValue", humidity / 10.0);
    cJSON_AddItemToObject(fields, "humidity", humidity_field);

    // 構建 temperature 字段
    cJSON *temperature_field = cJSON_CreateObject();
    cJSON_AddNumberToObject(temperature_field, "doubleValue", temperature / 10.0);
    cJSON_AddItemToObject(fields, "temperature", temperature_field);

    // 將 JSON 轉換為字符串
    char *json_data = cJSON_PrintUnformatted(root);
    cJSON_Delete(root);

    if (json_data == NULL) {
        fprintf(stderr, "Failed to create JSON data\n");
        return -1;
    }

    // 初始化 libcurl
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if(curl) {
        struct curl_slist *headers = NULL;
        // 設置 HTTP 標頭
        headers = curl_slist_append(headers, "Content-Type: application/json");
        char auth_header[512];
        snprintf(auth_header, sizeof(auth_header), "Authorization: Bearer %s", ACCESS_TOKEN);
        headers = curl_slist_append(headers, auth_header);

        // 設置 curl 選項
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data);

        // 執行請求
        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            ret = -1;
        }

        // 清理
        curl_slist_free_all(headers);
        curl_easy_cleanup(curl);
    } else {
        fprintf(stderr, "Failed to initialize curl\n");
        ret = -1;
    }

    curl_global_cleanup();
    free(json_data);
    return ret;
}

int main(void) {
    uint16_t humidity;
    int16_t temperature;

    // 初始化板子硬體
    BOARD_InitBootPins();
    BOARD_BootClockRUN();
    BOARD_InitDebugConsole(); // 初始化 Debug Console
    GPIO_Init();  // 初始化 GPIO

    while (1) {
        // 讀取 AM2120 資料
        AM2120_ReadData(&humidity, &temperature);
        // 打印讀取結果，根據感測器的精度進行適當的轉換
        PRINTF("Humidity: %.2f%%, Temperature: %.2f°C\r\n", humidity / 10.0, temperature / 10.0);
        // 上傳到 Firestore
        if(upload_to_firestore(humidity, temperature) != 0){
            PRINTF("Failed to upload data to Firestore\r\n");
        } else {
            PRINTF("Data uploaded to Firestore successfully\r\n");
        }
        // 每兩秒讀取一次
        SDK_DelayAtLeastUs(2000000, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);
    }
}
