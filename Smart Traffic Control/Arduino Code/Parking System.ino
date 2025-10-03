{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
\
//PARKING SYSTEM\
\
#include <SPI.h>\
#include <MFRC522.h>\
\
#define RST_PIN         9           \
#define SS_PIN          10          \
#define GREEN_LED_PIN   6   // Updated pin for green LED\
#define RED_LED_PIN     7   // Updated pin for red LED\
\
MFRC522 mfrc522(SS_PIN, RST_PIN);   \
\
unsigned long entryTimes[5] = \{0\};  // Store entry times for up to 5 cars\
int balanceBlock = 10;        // Block where the balance is stored\
long balanceAmount = 0;        // Stores the current balance\
int totalParkingSpaces = 5;   // Default parking space limit\
int availableSpaces = totalParkingSpaces;  // Available spaces\
\
MFRC522::MIFARE_Key key; // Authentication key for RFID\
\
// Array to store unique car numbers (up to 5 cars)\
String parkedCars[5];  // This will track up to 5 unique car numbers\
int numParkedCars = 0; // Count of currently parked cars\
\
void setup() \{\
  Serial.begin(9600); \
  SPI.begin();\
  mfrc522.PCD_Init(); \
  Serial.println(F("Parking system ready."));\
  \
  // Set the key to default (FFFFFFFFFFFF)\
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;\
  \
  // Initialize LED pins\
  pinMode(GREEN_LED_PIN, OUTPUT);\
  pinMode(RED_LED_PIN, OUTPUT);\
  \
  // Write initial balance to block 10 (200000)\
  balanceAmount = 200000;\
  writeBalanceToCard(balanceBlock, balanceAmount);\
\}\
\
void loop() \{\
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) \{\
    return;\
  \}\
\
  Serial.println(F("**Car Detected**"));\
\
  // Get the car number from block 2\
  String carNumber = getCarNumber();\
\
  if (carNumber == "") \{\
    Serial.println(F("Error reading car number!"));\
    return;\
  \}\
\
  Serial.print(F("Car Number: "));\
  Serial.println(carNumber);\
\
  // Check if the car is already parked (for entry or exit)\
  int carIndex = findCarIndex(carNumber);\
\
  if (carIndex == -1) \{  // New car trying to enter\
    if (availableSpaces <= 0) \{\
      Serial.println(F("Parking Full! No space available for new cars."));\
      blinkRedLED();\
    \} else \{\
      entryTimes[numParkedCars] = millis();  // Store entry time for the car\
      parkedCars[numParkedCars] = carNumber;\
      numParkedCars++;\
      availableSpaces--;\
\
      Serial.println(F("Car entered the parking lot."));\
      Serial.print(F("Available parking spaces: "));\
      Serial.println(availableSpaces);\
      \
      blinkGreenLED();\
    \}\
  \} else \{  // Car is already parked, so it\'92s exiting\
    unsigned long exitTime = millis();\
    unsigned long timeSpent = (exitTime - entryTimes[carIndex]) / 60000;  // Convert to minutes\
\
    Serial.print(F("Car exited the parking lot. Time spent: "));\
    Serial.print(timeSpent);\
    Serial.println(F(" minutes."));\
\
    removeParkedCar(carIndex);  // Remove car from parked list\
    availableSpaces++;\
    Serial.print(F("Available parking spaces: "));\
    Serial.println(availableSpaces);\
\
    deductParkingFee(timeSpent);  // Deduct balance based on time spent\
  \}\
\
  mfrc522.PICC_HaltA();\
  mfrc522.PCD_StopCrypto1();\
\}\
\
// Function to get the car number from block 2\
String getCarNumber() \{\
  MFRC522::StatusCode status;\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 2, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return "";\
  \}\
\
  byte buffer[18];\
  byte len = 18;\
  status = mfrc522.MIFARE_Read(2, buffer, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return "";\
  \}\
\
  String carNumber = "";\
  for (int i = 0; i < 16; i++) \{\
    if (buffer[i] != 32) \{\
      carNumber += char(buffer[i]);\
    \}\
  \}\
  return carNumber;\
\}\
\
// Function to find if the car is already parked\
int findCarIndex(String carNumber) \{\
  for (int i = 0; i < numParkedCars; i++) \{\
    if (parkedCars[i] == carNumber) \{\
      return i;\
    \}\
  \}\
  return -1;  // Car not found\
\}\
\
// Function to remove a car from the parkedCars array\
void removeParkedCar(int carIndex) \{\
  for (int i = carIndex; i < numParkedCars - 1; i++) \{\
    parkedCars[i] = parkedCars[i + 1];\
    entryTimes[i] = entryTimes[i + 1];\
  \}\
  numParkedCars--;\
\}\
\
// Function to deduct parking fee based on time spent\
void deductParkingFee(unsigned long timeSpent) \{\
  MFRC522::StatusCode status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, balanceBlock, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  byte buffer[18];\
  byte len = 18;\
  status = mfrc522.MIFARE_Read(balanceBlock, buffer, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  long balanceAmount = ((long)buffer[0] << 24) | ((long)buffer[1] << 16) | ((long)buffer[2] << 8) | buffer[3];\
  Serial.print("Current balance: ");\
  Serial.println(balanceAmount);\
\
  // Calculate amount to deduct based on time spent\
  int amountToDeduct = 0;\
  if (timeSpent < 1) \{\
    amountToDeduct = 5;  // Deduct 50 rupees if time spent is less than 1 minute\
  \} else \{\
    amountToDeduct = timeSpent * 10;  // Deduct 100 rupees per minute if time spent is 1 minute or more\
  \}\
\
  long newBalance = balanceAmount - amountToDeduct;\
\
  if (newBalance < 0) \{\
    Serial.println(F("Insufficient balance! Please recharge."));\
    return;\
  \}\
\
  Serial.print("New balance after deduction: ");\
  Serial.println(newBalance);\
\
  // Update balance on the card\
  writeBalanceToCard(balanceBlock, newBalance);\
\}\
\
// Function to write balance to the card\
void writeBalanceToCard(int blockNumber, long balance) \{\
  byte buffer[16];\
  \
  // Convert balance to 4 bytes\
  buffer[0] = (balance >> 24) & 0xFF;\
  buffer[1] = (balance >> 16) & 0xFF;\
  buffer[2] = (balance >> 8) & 0xFF;\
  buffer[3] = balance & 0xFF;\
\
  // Fill the rest of the block with zeros\
  for (int i = 4; i < 16; i++) \{\
    buffer[i] = 0;\
  \}\
\
  MFRC522::StatusCode status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNumber, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Write(blockNumber, buffer, 16);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Writing failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\}\
\
// Function to blink the green LED\
void blinkGreenLED() \{\
  digitalWrite(GREEN_LED_PIN, HIGH);\
  delay(2000);\
  digitalWrite(GREEN_LED_PIN, LOW);\
\}\
\
// Function to blink the red LED\
void blinkRedLED() \{\
  digitalWrite(RED_LED_PIN, HIGH);\
  delay(2000);\
  digitalWrite(RED_LED_PIN, LOW);\
\}\
\
\
\
\
\
}
