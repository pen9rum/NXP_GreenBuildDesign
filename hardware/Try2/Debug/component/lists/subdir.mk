################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../component/lists/fsl_component_generic_list.c 

C_DEPS += \
./component/lists/fsl_component_generic_list.d 

OBJS += \
./component/lists/fsl_component_generic_list.o 


# Each subdirectory must supply rules for building sources it contributes
component/lists/%.o: ../component/lists/%.c component/lists/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: MCU C Compiler'
	arm-none-eabi-gcc -D__REDLIB__ -DCPU_MIMXRT1062DVL6B -DCPU_MIMXRT1062DVL6B_cm7 -DSDK_OS_BAREMETAL -DXIP_EXTERNAL_FLASH=1 -DXIP_BOOT_HEADER_ENABLE=1 -DSDK_DEBUGCONSOLE=1 -DCR_INTEGER_PRINTF -DPRINTF_FLOAT_ENABLE=0 -DSERIAL_PORT_TYPE_UART=1 -D__MCUXPRESSO -D__USE_CMSIS -DDEBUG -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\board" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\source" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\utilities" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\component\lists" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\component\serial_manager" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\CMSIS" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\drivers" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\xip" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\component\uart" -I"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Try2\device" -O0 -fno-common -g3 -gdwarf-4 -Wall -c -ffunction-sections -fdata-sections -fno-builtin -fmerge-constants -fmacro-prefix-map="$(<D)/"= -mcpu=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -D__REDLIB__ -fstack-usage -specs=redlib.specs -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.o)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


clean: clean-component-2f-lists

clean-component-2f-lists:
	-$(RM) ./component/lists/fsl_component_generic_list.d ./component/lists/fsl_component_generic_list.o

.PHONY: clean-component-2f-lists

