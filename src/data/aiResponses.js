export const SUGGEST_PROMPTS = [
  "How do I recover a failed sensor?",
  "Configure new motor controller",
  "Help with pin mapping",
  "Field deployment guide",
];

export const AI_RESPONSES = {
  "How do I recover a failed sensor?": `To recover a failed sensor:\n\n1. Check the physical connection and power supply.\n2. Run diagnostics from the Monitoring tab.\n3. Use the Auto-Recover button if available.\n4. If still failing, trigger a 'Signal reset + calibration' workflow.\n5. Check logs for root cause.\n\nFor persistent failures, consider replacing the sensor and updating the recovery workflow in the Workflows tab.`,

  "Configure new motor controller": `To configure a new motor controller:\n\n1. Go to the Configure tab.\n2. Add a new component with type 'Actuator'.\n3. Set pin configuration (e.g., PWM 5, 6, 9, 10).\n4. Describe the control logic in the Control Behavior section.\n5. Click 'Generate Control Logic' to let AI create the control summary.\n6. Click 'Deploy to System' when ready.\n\nThe system will auto-generate recovery workflows for the new controller.`,

  "Help with pin mapping": `Pin mapping guide for common components:\n\n• IMU Sensors → I2C on GPIO 14, 15\n• Motor Controllers → PWM on pins 5, 6, 9, 10\n• GPS/UART devices → TX/RX on pins 8,9 or 16,17\n• Camera → CSI Interface\n• Servo/Gripper → Single PWM pin (e.g., PWM 12)\n\nAvoid pin conflicts by checking the Configure tab's current components list before adding new hardware.`,

  "Field deployment guide": `Field deployment checklist:\n\n1. Verify all devices show 'online' in the Monitoring tab.\n2. Run diagnostics on any 'warning' status devices.\n3. Confirm Mission Objective is set in the Configure tab.\n4. Deploy active Workflows for auto-recovery scenarios.\n5. Check Analytics to confirm >95% uptime baseline.\n6. Set up 'Send Alert' actions for offline triggers.\n7. Test Auto-Recover on non-critical components first.\n8. Ensure all recovery protocols are deployed before field ops.`,
};

export const DEFAULT_AI_RESPONSE = (text) =>
  `I understand you're asking about "${text}". As your AI Copilot, I can help you configure hardware, troubleshoot devices, and optimize your robotic system.\n\nCould you provide more details about what specific issue you're experiencing? You can also use the quick prompts below for common tasks.`;
