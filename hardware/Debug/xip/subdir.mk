################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../xip/evkbmimxrt1060_flexspi_nor_config.c \
../xip/fsl_flexspi_nor_boot.c 

C_DEPS += \
./xip/evkbmimxrt1060_flexspi_nor_config.d \
./xip/fsl_flexspi_nor_boot.d 

OBJS += \
./xip/evkbmimxrt1060_flexspi_nor_config.o \
./xip/fsl_flexspi_nor_boot.o 


# Each subdirectory must supply rules for building sources it contributes
xip/%.o: ../xip/%.c xip/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__REDLIB__ -DCPU_MIMXRT1062DVL6B -DCPU_MIMXRT1062DVL6B_cm7 -DSDK_OS_BAREMETAL -DXIP_EXTERNAL_FLASH=1 -DXIP_BOOT_HEADER_ENABLE=1 -DSDK_DEBUGCONSOLE=1 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -DSERIAL_PORT_TYPE_UART=1 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\board" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\mongoose" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\mongo-c-driver-1.28.1\src\libbson" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\mongo-c-driver-1.28.1" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\FATFS" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\source" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\utilities" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\component\lists" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\component\serial_manager" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\CMSIS" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\drivers" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\xip" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\component\uart" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\device" -include"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\FATFS\source\ff.h" -O0 -fno-common -g3 -gdwarf-4 -Wall -c -ffunction-sections -fdata-sections -fno-builtin -fmerge-constants -fmacro-prefix-map="$(<D)/"= -mcpu=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


clean: clean-xip

clean-xip:
	-$(RM) ./xip/evkbmimxrt1060_flexspi_nor_config.d ./xip/evkbmimxrt1060_flexspi_nor_config.o ./xip/fsl_flexspi_nor_boot.d ./xip/fsl_flexspi_nor_boot.o

.PHONY: clean-xip

