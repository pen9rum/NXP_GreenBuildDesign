#include <stdio.h>
#include <time.h>           // 用於時間戳
#include "board.h"
#include "peripherals.h"
#include "pin_mux.h"
#include "clock_config.h"
#include "fsl_gpio.h"    // GPIO 驅動的頭文件
#include "fsl_iomuxc.h"  // IOMUXC 驅動的頭文件
#include "fsl_debug_console.h"
#include "mongoose_config.h"  // 確保在 mongoose.h 之前
#include "mongoose.h"

#define AM2120_PIN 3U  // 使用 GPIO_AD_B0_03

static const char *s_http_port = "5173";

// HTTP 請求處理函數
static void ev_handler(struct mg_connection *nc, int ev, void *ev_data) {
    struct http_message *hm = (struct http_message *)ev_data;

    if (ev == MG_EV_HTTP_REQUEST) {
        if (mg_vcmp(&hm->uri, "/api/getData") == 0) {
            if (mg_vcmp(&hm->method, "POST") == 0) {
                uint8_t humidity = 0, temperature = 0;
                AM2120_ReadData(&humidity, &temperature);

                time_t t = time(NULL);
                struct tm *tm_info = localtime(&t);
                char timeStr[25];
                strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", tm_info);

                char response[256];
                snprintf(response, sizeof(response),
                         "{ \"time\": \"%s\", \"humidity\": %d, \"temperature\": %d }",
                         timeStr, humidity, temperature);

                mg_send_head(nc, 200, strlen(response), "Content-Type: application/json");
                mg_printf(nc, "%s", response);
            } else {
                mg_send_head(nc, 405, 0, "Content-Type: text/plain");
                mg_printf(nc, "Method Not Allowed");
            }
        } else {
            mg_send_head(nc, 404, 0, "Content-Type: text/plain");
            mg_printf(nc, "Not Found");
        }
    }
}

void GPIO_Init(void) {
    gpio_pin_config_t config = {
        kGPIO_DigitalInput, 0,
    };
    IOMUXC_SetPinMux(IOMUXC_GPIO_AD_B0_03_GPIO1_IO03, 0U);
    IOMUXC_SetPinConfig(IOMUXC_GPIO_AD_B0_03_GPIO1_IO03,
        IOMUXC_SW_PAD_CTL_PAD_PKE_MASK |
        IOMUXC_SW_PAD_CTL_PAD_PUE_MASK |
        IOMUXC_SW_PAD_CTL_PAD_PUS(2U) |
        IOMUXC_SW_PAD_CTL_PAD_DSE(6U) |
        IOMUXC_SW_PAD_CTL_PAD_SPEED(2U)
    );
    GPIO_PinInit(GPIO1, AM2120_PIN, &config);
}

void AM2120_StartSignal(void) {
    gpio_pin_config_t config = {
        kGPIO_DigitalOutput, 0,
    };
    GPIO_PinInit(GPIO1, AM2120_PIN, &config);
    GPIO_PinWrite(GPIO1, AM2120_PIN, 0);
    SDK_DelayAtLeastUs(2000, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);

    GPIO_PinWrite(GPIO1, AM2120_PIN, 1);
    SDK_DelayAtLeastUs(40, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);

    config.direction = kGPIO_DigitalInput;
    GPIO_PinInit(GPIO1, AM2120_PIN, &config);
}

uint8_t AM2120_ReadBit(void) {
    while (GPIO_PinRead(GPIO1, AM2120_PIN) == 1);
    SDK_DelayAtLeastUs(30, SDK_DEVICE_MAXIMUM_CPU_CLOCK_FREQUENCY);
    return GPIO_PinRead(GPIO1, AM2120_PIN);
}

void AM2120_ReadData(uint8_t *humidity, uint8_t *temperature) {
    uint8_t data[5] = {0};
    AM2120_StartSignal();

    for (int i = 0; i < 40; i++) {
        data[i / 8] <<= 1;
        data[i / 8] |= AM2120_ReadBit();
    }

    *humidity = data[0];
    *temperature = data[2];
    uint8_t checksum = data[0] + data[1] + data[2] + data[3];
    if (checksum != data[4]) {
        PRINTF("Check sum error: humidity=%d, temperature=%d, checksum=%d\r\n", *humidity, *temperature, data[4]);
    }
}

int main(void) {
    struct mg_mgr mgr;
    struct mg_connection *nc;

    BOARD_InitBootPins();
    BOARD_BootClockRUN();
    BOARD_InitDebugConsole();
    GPIO_Init();

    mg_mgr_init(&mgr, NULL);
    nc = mg_bind(&mgr, s_http_port, ev_handler);
    mg_set_protocol_http_websocket(nc);

    printf("HTTP server started on port %s\n", s_http_port);
    while (1) {
        mg_mgr_poll(&mgr, 1000);
    }
    mg_mgr_free(&mgr);

    return 0;
}
