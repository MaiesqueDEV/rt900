.syntax unified
.cpu cortex-m0
.thumb

.global g_pfnVectors
.global Default_Handler
.global Reset_Handler

/* Vector Table */
.section .isr_vector, "a", %progbits
.type g_pfnVectors, %object
.size g_pfnVectors, .-g_pfnVectors

g_pfnVectors:
    .word   _estack                       /* Top of Stack */
    .word   Reset_Handler                 /* Reset Handler */
    .word   NMI_Handler                   /* NMI Handler */
    .word   HardFault_Handler             /* Hard Fault Handler */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   SVC_Handler                   /* SVCall Handler */
    .word   0                             /* Reserved */
    .word   0                             /* Reserved */
    .word   PendSV_Handler                /* PendSV Handler */
    .word   SysTick_Handler               /* SysTick Handler */

    /* External Interrupts (BT32F0x) */
    .word   WWDG_IRQHandler               /* 0: Window Watchdog */
    .word   PVD_IRQHandler                /* 1: PVD through EXTI Line detect */
    .word   RTC_IRQHandler                /* 2: RTC through EXTI Line */
    .word   FLASH_IRQHandler              /* 3: FLASH */
    .word   RCC_IRQHandler                /* 4: RCC */
    .word   EXTI0_1_IRQHandler            /* 5: EXTI Line 0 and 1 */
    .word   EXTI2_3_IRQHandler            /* 6: EXTI Line 2 and 3 */
    .word   EXTI4_15_IRQHandler           /* 7: EXTI Line 4 to 15 */
    .word   TS_IRQHandler                 /* 8: TS */
    .word   DMA1_Channel1_IRQHandler      /* 9: DMA1 Channel 1 */
    .word   DMA1_Channel2_3_IRQHandler    /* 10: DMA1 Channel 2 and Channel 3 */
    .word   DMA1_Channel4_5_IRQHandler    /* 11: DMA1 Channel 4 and Channel 5 */
    .word   ADC1_COMP_IRQHandler          /* 12: ADC1, COMP1 and COMP2 */
    .word   TIM1_BRK_UP_TRG_COM_IRQHandler/* 13: TIM1 Break, Update, Trigger and Commutation */
    .word   TIM1_CC_IRQHandler            /* 14: TIM1 Capture Compare */
    .word   TIM2_IRQHandler               /* 15: TIM2 */
    .word   TIM3_IRQHandler               /* 16: TIM3 */
    .word   TIM6_IRQHandler               /* 17: TIM6 */
    .word   TIM7_IRQHandler               /* 18: TIM7 */
    .word   TIM14_IRQHandler              /* 19: TIM14 */
    .word   TIM15_IRQHandler              /* 20: TIM15 */
    .word   TIM16_IRQHandler              /* 21: TIM16 */
    .word   TIM17_IRQHandler              /* 22: TIM17 */
    .word   I2C1_IRQHandler               /* 23: I2C1 */
    .word   I2C2_IRQHandler               /* 24: I2C2 */
    .word   SPI1_IRQHandler               /* 25: SPI1 */
    .word   SPI2_IRQHandler               /* 26: SPI2 */
    .word   USART1_IRQHandler             /* 27: USART1 */
    .word   USART2_IRQHandler             /* 28: USART2 */
    .word   USART3_6IRQHandler            /* 29: USART3_6 */
    .word   ALU_IRQHandler                /* 30: ALU */
    .word   0                             /* 31: Reserved */

.text
.thumb
.thumb_func

/* Reset Handler */
.type Reset_Handler, %function
Reset_Handler:
    /* Set stack pointer to top of stack */
    ldr   r0, =_estack
    mov   sp, r0

    /* 1. Copy initialized .data section from FLASH to SRAM */
    ldr   r1, =_sdata
    ldr   r2, =_edata
    ldr   r3, =_sidata
    b     LoopCopyData

CopyData:
    ldr   r4, [r3]
    str   r4, [r1]
    adds  r3, r3, #4
    adds  r1, r1, #4

LoopCopyData:
    cmp   r1, r2
    bcc   CopyData

    /* 2. Zero fill the .bss section in SRAM */
    ldr   r1, =_sbss
    ldr   r2, =_ebss
    movs  r3, #0
    b     LoopZeroBss

ZeroBss:
    str   r3, [r1]
    adds  r1, r1, #4

LoopZeroBss:
    cmp   r1, r2
    bcc   ZeroBss

    /* 3. Call SystemInit() */
    ldr   r0, =SystemInit
    blx   r0

    /* 4. Call main() */
    ldr   r0, =main
    blx   r0

    /* Infinite loop if main ever returns */
InfiniteLoop:
    b     InfiniteLoop
.size Reset_Handler, .-Reset_Handler

/* Default Handler for unhandled exceptions/interrupts */
.type Default_Handler, %function
Default_Handler:
Infinite_Loop:
    b     Infinite_Loop
.size Default_Handler, .-Default_Handler

/* Weak definitions of exception handlers */
.weak NMI_Handler
.thumb_set NMI_Handler, Default_Handler

.weak HardFault_Handler
.thumb_set HardFault_Handler, Default_Handler

.weak SVC_Handler
.thumb_set SVC_Handler, Default_Handler

.weak PendSV_Handler
.thumb_set PendSV_Handler, Default_Handler

.weak SysTick_Handler
.thumb_set SysTick_Handler, Default_Handler

/* Weak definitions of interrupt handlers */
.weak WWDG_IRQHandler
.thumb_set WWDG_IRQHandler, Default_Handler

.weak PVD_IRQHandler
.thumb_set PVD_IRQHandler, Default_Handler

.weak RTC_IRQHandler
.thumb_set RTC_IRQHandler, Default_Handler

.weak FLASH_IRQHandler
.thumb_set FLASH_IRQHandler, Default_Handler

.weak RCC_IRQHandler
.thumb_set RCC_IRQHandler, Default_Handler

.weak EXTI0_1_IRQHandler
.thumb_set EXTI0_1_IRQHandler, Default_Handler

.weak EXTI2_3_IRQHandler
.thumb_set EXTI2_3_IRQHandler, Default_Handler

.weak EXTI4_15_IRQHandler
.thumb_set EXTI4_15_IRQHandler, Default_Handler

.weak TS_IRQHandler
.thumb_set TS_IRQHandler, Default_Handler

.weak DMA1_Channel1_IRQHandler
.thumb_set DMA1_Channel1_IRQHandler, Default_Handler

.weak DMA1_Channel2_3_IRQHandler
.thumb_set DMA1_Channel2_3_IRQHandler, Default_Handler

.weak DMA1_Channel4_5_IRQHandler
.thumb_set DMA1_Channel4_5_IRQHandler, Default_Handler

.weak ADC1_COMP_IRQHandler
.thumb_set ADC1_COMP_IRQHandler, Default_Handler

.weak TIM1_BRK_UP_TRG_COM_IRQHandler
.thumb_set TIM1_BRK_UP_TRG_COM_IRQHandler, Default_Handler

.weak TIM1_CC_IRQHandler
.thumb_set TIM1_CC_IRQHandler, Default_Handler

.weak TIM2_IRQHandler
.thumb_set TIM2_IRQHandler, Default_Handler

.weak TIM3_IRQHandler
.thumb_set TIM3_IRQHandler, Default_Handler

.weak TIM6_IRQHandler
.thumb_set TIM6_IRQHandler, Default_Handler

.weak TIM7_IRQHandler
.thumb_set TIM7_IRQHandler, Default_Handler

.weak TIM14_IRQHandler
.thumb_set TIM14_IRQHandler, Default_Handler

.weak TIM15_IRQHandler
.thumb_set TIM15_IRQHandler, Default_Handler

.weak TIM16_IRQHandler
.thumb_set TIM16_IRQHandler, Default_Handler

.weak TIM17_IRQHandler
.thumb_set TIM17_IRQHandler, Default_Handler

.weak I2C1_IRQHandler
.thumb_set I2C1_IRQHandler, Default_Handler

.weak I2C2_IRQHandler
.thumb_set I2C2_IRQHandler, Default_Handler

.weak SPI1_IRQHandler
.thumb_set SPI1_IRQHandler, Default_Handler

.weak SPI2_IRQHandler
.thumb_set SPI2_IRQHandler, Default_Handler

.weak USART1_IRQHandler
.thumb_set USART1_IRQHandler, Default_Handler

.weak USART2_IRQHandler
.thumb_set USART2_IRQHandler, Default_Handler

.weak USART3_6IRQHandler
.thumb_set USART3_6IRQHandler, Default_Handler

.weak ALU_IRQHandler
.thumb_set ALU_IRQHandler, Default_Handler

.end
