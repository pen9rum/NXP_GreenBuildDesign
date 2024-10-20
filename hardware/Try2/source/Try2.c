#include <stdio.h>
#include "board.h"
#include "peripherals.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "fsl_gpio.h"
#include "fsl_iomuxc.h"
#include "fsl_debug_console.h"
#include <time.h>

#define AM2120_PIN 3U  // 使用 GPIO_AD_B0_03

void GPIO_Init(void) {
    gpio_pin_config_t config = {
        kGPIO_DigitalInput, 0, // 初始化為輸入
    };

    // 設定引腳多工功能為 GPIO
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_B0_03_GPIO1_IO03, 0U);

    // 配置引腳的電氣參數
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_B0_03_GPIO1_IO03,
        IOMUXC_SW_PAD_CTL_PAD_PKE_MASK |
        IOMUXC_SW_PAD_CTL_PAD_PUE_MASK |
        IOMUXC_SW_PAD_CTL_PAD_PUS(2U) |
        IOMUXC_SW_PAD_CTL_PAD_DSE(6U) |
        IOMUXC_SW_PAD_CTL_PAD_SPEED(2U)
    );

    // 初始化 GPIO
//    if (GPIO_PinInit(GPIO1, AM2120_PIN, &config) != kStatus_Success) {
//        PRINTF("GPIO initialization failed!\r\n");
//        // while (1); // 無法初始化，進入死循環
//    }
}

void AM2120_StartSignal(void) {
    gpio_pin_config_t config = {
        kGPIO_DigitalOutput, 0, // 設為輸出
    };
    GPIO_PinInit(GPIO1, AM2120_PIN, &config);

    // 拉低引腳超過 1ms
    GPIO_PinWrite(GPIO1, AM2120_PIN, 0);
    SDK_DelayAtLeastUs(2000, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);  // 2ms 延遲

    // 恢復高電平
    GPIO_PinWrite(GPIO1, AM2120_PIN, 1);
    SDK_DelayAtLeastUs(40, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);  // 延遲 40µs

    // 設置引腳為輸入，準備接收數據
    config.direction = kGPIO_DigitalInput;
    GPIO_PinInit(GPIO1, AM2120_PIN, &config);
}

uint8_t AM2120_ReadBit(void) {
    // 等待 AM2120 準備好，會給出一個低電平開始信號
    while (GPIO_PinRead(GPIO1, AM2120_PIN) == 1);

    // 延遲約 30µs 判斷資料（0 或 1）
    SDK_DelayAtLeastUs(30, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);
    return GPIO_PinRead(GPIO1, AM2120_PIN);
}

void AM2120_ReadData(uint16_t *humidity, int16_t *temperature) {
    uint8_t data[5] = {0};
    AM2120_StartSignal(); // 發送開始信號

    // 讀取 40 位資料 (5 bytes)
    for (int i = 0; i < 40; i++) {
        // Introducing a small delay to ensure proper synchronization
        SDK_DelayAtLeastUs(1, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);

        data[i / 8] <<= 1;
        data[i / 8] |= AM2120_ReadBit();
    }
    gpio_pin_config_t config = {
        kGPIO_DigitalOutput, 0, // 設為輸出
    };
    GPIO_PinInit(GPIO1, AM2120_PIN, &config);
    GPIO_PinWrite(GPIO1, AM2120_PIN, 1);

    // 濕度數據解析
    uint16_t raw_humidity = (data[0] << 8) | data[1];
    *humidity = raw_humidity / 10; // 轉換為實際濕度值

    // 溫度數據解析
    uint16_t raw_temperature = (data[2] << 8) | data[3];
    *temperature = (raw_temperature & 0x7FFF) / 10; // 轉換為實際溫度值

    // 如果第 15 位是 1，表示負溫度
    if (raw_temperature & 0x8000) {
        *temperature = -*temperature;
    }

    // 校驗和檢查
//    uint8_t checksum = data[0] + data[1] + data[2] + data[3];
//    if (checksum != data[4]) {
//        PRINTF("Check sum error: humidity=%d, temperature=%d, checksum=%d, raw=%02X %02X %02X %02X %02X\r\n",
//               *humidity, *temperature, data[4], data[0], data[1], data[2], data[3], data[4]);
//    } else {
//        PRINTF("Data OK: humidity=%d, temperature=%d\r\n", *humidity, *temperature);
//    }
}




int main(void) {
    uint8_t humidity, temperature;

    // 初始化板子硬體
    BOARD_InitBootPins();
    BOARD_BootClockRUN();
    BOARD_InitDebugConsole(); // 初始化 Debug Console
    GPIO_Init();  // 初始化 GPIO

    while (1) {
        // 讀取 AM2120 資料
        AM2120_ReadData(&humidity, &temperature);

        // 格式化時間戳記為 ISO 8601 格式

        // 打印讀取結果以 JSON 格式
        PRINTF("{\"humidity\": %d, \"temperature\": %d}\r\n",
                humidity, temperature);

        // 每兩秒讀取一次
        SDK_DelayAtLeastUs(3000000, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);
    }
}
