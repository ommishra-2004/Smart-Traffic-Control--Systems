{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 //TOLLING SYSTEM\
\
#include <SPI.h>\
#include <MFRC522.h>\
\
#define RST_PIN 9     // Configurable, see typical pin layout above\
#define SS_PIN 10     // Configurable, see typical pin layout above\
\
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance\
\
//*****************************************************************************************//\
void setup() \{\
  Serial.begin(9600);                                           // Initialize serial communications with the PC\
  SPI.begin();                                                  // Init SPI bus\
  mfrc522.PCD_Init();                                           // Init MFRC522 card\
  Serial.println(F("Read personal data on a MIFARE PICC:"));    // Shows in serial that it is ready to read\
\}\
\
//*****************************************************************************************//\
void loop() \{\
  MFRC522::MIFARE_Key key;\
  for (byte i = 0; i < 6; i++) key.keyByte[i] = 0xFF;  // Default key (factory setting)\
\
  byte block;\
  byte len;\
  MFRC522::StatusCode status;\
\
  if (!mfrc522.PICC_IsNewCardPresent()) return;\
  if (!mfrc522.PICC_ReadCardSerial()) return;\
\
  Serial.println(F("\\nCAR DETECTED "));\
\
  Serial.print(F("CAR NUMBER: "));\
\
  byte buffer1[18];\
  block = 2;\
  len = 18;\
\
  // Authenticate and Read CAR NUMBER\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Read(block, buffer1, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  for (uint8_t i = 0; i < 16; i++) \{\
    if (buffer1[i] != 32) Serial.write(buffer1[i]);\
  \}\
  Serial.println();\
\
  // Read NAME\
  Serial.print(F("NAME: "));\
  byte buffer3[18];\
  block = 8;\
  len = 18;\
\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Read(block, buffer3, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  for (uint8_t i = 0; i < 16; i++) \{\
    if (buffer3[i] != 32) Serial.write(buffer3[i]);\
  \}\
  Serial.println();\
\
  // Read CAR MODEL\
  Serial.print(F("CAR MODEL: "));\
  byte buffer4[18];\
  block = 1;\
  len = 18;\
\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Read(block, buffer4, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  for (uint8_t i = 0; i < 16; i++) \{\
    if (buffer4[i] != 32) Serial.write(buffer4[i]);\
  \}\
  Serial.println();\
\
/*\
Serial.print(F("CAR COLOR : "));\
byte buffer5[18];\
\
  block = 4;\
  len = 18;\
\
  //------------------------------------------- GET COLOR\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 4, &key, &(mfrc522.uid)); //line 834 of MFRC522.cpp file\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Read(block, buffer5, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  //PRINT NAME\
  for (uint8_t i = 0; i < 16; i++)\
  \{\
    if (buffer5[i] != 32)\
    \{\
      Serial.write(buffer5[i]); \
    \}\
  \}\
    Serial.println();\
\
\
    Serial.print(F("AADHAR NUMBER : "));\
\
  byte buffer2[18];\
  block = 5;\
\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, 5, &key, &(mfrc522.uid)); //line 834\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Read(block, buffer2, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  //PRINT AADHAR NUMBER\
  for (uint8_t i = 0; i < 16; i++) \{\
    Serial.write(buffer2[i] );\
  \}\
    Serial.println(" ");\
\
*/\
\
  // Read and update BALANCE AMOUNT\
  byte buffer6[18];\
  block = 10;\
  len = 18;\
\
  status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, block, &key, &(mfrc522.uid));\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Authentication failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  status = mfrc522.MIFARE_Read(block, buffer6, &len);\
  if (status != MFRC522::STATUS_OK) \{\
    Serial.print(F("Reading failed: "));\
    Serial.println(mfrc522.GetStatusCodeName(status));\
    return;\
  \}\
\
  // Retrieve and print the balance value\
  long storedValue = ((long)buffer6[0] << 24) | ((long)buffer6[1] << 16) | ((long)buffer6[2] << 8) | buffer6[3];\
  Serial.print("BALANCE AMOUNT: ");\
  Serial.println(storedValue);\
\
  if (storedValue < 500) \{\
    Serial.println("!!PLEASE RECHARGE YOUR TAG!!");\
  \} else \{\
    long newValue = storedValue - 500;\
    Serial.print("BALANCE AFTER DEDUCTION: ");\
    Serial.println(newValue);\
\
    // Update buffer6 to store the new balance in 4 bytes\
    buffer6[0] = (newValue >> 24) & 0xFF;\
    buffer6[1] = (newValue >> 16) & 0xFF;\
    buffer6[2] = (newValue >> 8) & 0xFF;\
    buffer6[3] = newValue & 0xFF;\
\
    // Write the updated balance back to block 10\
    status = mfrc522.MIFARE_Write(block, buffer6, 16);\
    if (status != MFRC522::STATUS_OK) \{\
      Serial.print(F("Writing failed: "));\
      Serial.println(mfrc522.GetStatusCodeName(status));\
      return;\
    \}\
\
    Serial.println(F("TOLL DEDUCTED SUCCESSFULLY AND CHECK YOUR ACCOUNT FOR UPDATED DETAILS, THANK YOU !!!"));\
  \}\
\
  delay(10);\
\
  mfrc522.PICC_HaltA();\
  mfrc522.PCD_StopCrypto1();\
\}\
\
}
