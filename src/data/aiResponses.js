export const SUGGEST_PROMPTS = [
  "Turn on LED on pin 17",
  "Rotate servo on pin 12 to 90 degrees",
  "Start reading sensor on pin 23",
  "Turn off motor on pin 18",
];

export const AI_RESPONSES = {
  "Connect IMU sensor to GPIO 2":
    "✅ IMU Sensor Configuration\n\nI'll set up your IMU sensor (MPU6050) on GPIO 2 using the I2C protocol.\n\nHere's the plan:\n• Protocol: I2C (SDA: GPIO 2, SCL: GPIO 3)\n• Address: 0x68 (default)\n• Sample rate: 100Hz\n• Data: Accelerometer (±2g) + Gyroscope (±250°/s)\n\nI've generated the control logic. You can review and deploy it from the Configure tab.",

  "Setup motor on pin 18":
    "✅ Motor Configuration\n\nI'll configure a PWM-controlled motor on GPIO 18.\n\nSetup details:\n• Pin: GPIO 18 (hardware PWM capable)\n• Frequency: 1000Hz\n• Initial duty cycle: 0% (stopped)\n• Direction control: Requires additional GPIO for H-bridge\n\n⚠️ Safety Note: Make sure your motor driver (L298N or similar) is properly connected. Never connect a motor directly to GPIO pins.\n\nReady to deploy from the Configure tab.",

  "Recover offline LiDAR":
    "🔧 LiDAR Recovery Protocol\n\nI've detected that your LiDAR sensor has been offline for approximately 2 hours. Here's my recovery plan:\n\n1. Power Cycle — Toggle VCC pin to reset the sensor\n2. I2C Bus Reset — Clear any stuck communication lines\n3. Re-initialize — Send configuration commands\n4. Verify — Take test measurements to confirm operation\n\nEstimated recovery time: ~15 seconds\n\nShall I execute this recovery sequence?",

  "Explain PID control":
    "📚 PID Control Explained\n\nPID (Proportional-Integral-Derivative) is a control algorithm widely used in robotics:\n\n• P (Proportional): Reacts to current error. Bigger error = stronger correction.\n\n• I (Integral): Accumulates past errors. Fixes steady-state offset over time.\n\n• D (Derivative): Predicts future error based on rate of change. Reduces overshoot.\n\nFormula: output = Kp×error + Ki×∫error + Kd×(d/dt)error\n\nIn your drone system, PID controls:\n→ Roll/Pitch stabilization using IMU data\n→ Altitude hold using barometer readings\n→ Yaw control using magnetometer/gyro\n\nEach axis needs its own PID tuning (Kp, Ki, Kd values).",
};

export const DEFAULT_AI_RESPONSE = (input) =>
  `🤖 Processing: "${input}"\n\nI've analyzed your request. Here's what I can do:\n\n1. Parse the intent and identify relevant hardware components\n2. Generate appropriate control logic with safety validation\n3. Apply the configuration to your connected devices\n\nFor this specific request, I recommend heading to the Configure tab where you can set up the components and deploy the generated logic.\n\nWould you like me to elaborate on any specific aspect?`;
