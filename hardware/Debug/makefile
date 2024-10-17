################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include xip/subdir.mk
-include utilities/subdir.mk
-include startup/subdir.mk
-include source/subdir.mk
-include drivers/subdir.mk
-include device/subdir.mk
-include component/uart/subdir.mk
-include component/serial_manager/subdir.mk
-include component/lists/subdir.mk
-include board/subdir.mk
ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := Hackerthon
BUILD_ARTIFACT_EXTENSION := axf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all:
	+@$(MAKE) --no-print-directory main-build && $(MAKE) --no-print-directory post-build

# Main-build Target
main-build: Hackerthon.axf

# Tool invocations
Hackerthon.axf: $(OBJS) $(USER_OBJS) makefile $(OPTIONAL_TOOL_DEPS)
	@echo 'Building target: $@'
	@echo 'Invoking: MCU Linker'
	arm-none-eabi-gcc -nostdlib -L"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\mongo-c-driver-1.28.1" -Xlinker -Map="Hackerthon.map" -Xlinker --gc-sections -Xlinker -print-memory-usage -Xlinker --sort-section=alignment -Xlinker --cref -mcpu=cortex-m7 -mfpu=fpv5-sp-d16 -mfloat-abi=hard -mthumb -T Hackerthon_Debug.ld -o "Hackerthon.axf" $(OBJS) $(USER_OBJS) $(LIBS) -l"C:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\mongo-c-driver-1.28.1" -lC:\Users\USER\Documents\MCUXpressoIDE_11.10.0_3148\workspace\Hackerthon\mongo-c-driver-1.28.1\src\libbson
	@echo 'Finished building target: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) Hackerthon.axf
	-@echo ' '

post-build:
	-@echo 'Performing post-build steps'
	-arm-none-eabi-size "Hackerthon.axf"; # arm-none-eabi-objcopy -v -O binary "Hackerthon.axf" "Hackerthon.bin" ; # checksum -p MIMXRT1062xxxxB -d "Hackerthon.bin";
	-@echo ' '

.PHONY: all clean dependents main-build post-build

-include ../makefile.targets
