#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9 // Using pin 9 as per your project files
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

// =======================================================================
// +++ UPDATE THE VEHICLE DETAILS FOR THE CARD YOU WANT TO PROGRAM +++
// =======================================================================
String vehicleModel    = "Toyota Camry";
String vehicleNumber   = "MH04AB1234";
String vehicleColor    = "Blue";
String aadharNumber    = "1234 5678 9012";
String emergencyStatus = ""; // Leave blank, or set to "EMERGENCY"
String ownerName       = "John Doe";
long   accountBalance  = 2000;
// =======================================================================

void setup() {
    Serial.begin(9600);
    SPI.begin();
    mfrc522.PCD_Init();
    
    // Set the default security key for new cards
    for (byte i = 0; i < 6; i++) {
        key.keyByte[i] = 0xFF;
    }
    
    Serial.println("--- Universal Vehicle Card Programmer ---");
    Serial.println("Bring a card near the reader to write all data at once.");
}

void loop() {
    // Look for a new card
    if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) {
        delay(50);
        return;
    }

    Serial.println("\n---------------------------------");
    Serial.println("Card Detected! Starting write process...");

    // --- Write all data blocks sequentially ---
    writeStringToBlock(1, vehicleModel);
    writeStringToBlock(2, vehicleNumber);
    writeStringToBlock(4, vehicleColor);
    writeStringToBlock(5, aadharNumber);
    writeStringToBlock(6, emergencyStatus);
    writeStringToBlock(8, ownerName);
    writeLongToBlock(10, accountBalance);

    // --- End of write process ---
    
    Serial.println("All data has been written successfully!");
    Serial.println("---------------------------------");
    Serial.println("Ready for the next card.");

    // Halt the card and wait before programming the next one
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
    delay(3000); // Wait 3 seconds
}

// Helper function to write a String to a specific block
void writeStringToBlock(int blockNumber, const String& textData) {
    byte dataBuffer[16] = {0}; // Initialize buffer with zeros
    textData.getBytes(dataBuffer, 17); // Convert String to byte array
    
    if (writeBlock(blockNumber, dataBuffer)) {
        Serial.print(" -> Wrote \"");
        Serial.print(textData);
        Serial.print("\" to block ");
        Serial.println(blockNumber);
    }
}

// Helper function to write a long integer to a specific block
void writeLongToBlock(int blockNumber, long numericData) {
    byte dataBuffer[16] = {0}; // Initialize buffer with zeros
    dataBuffer[0] = (numericData >> 24) & 0xFF;
    dataBuffer[1] = (numericData >> 16) & 0xFF;
    dataBuffer[2] = (numericData >> 8) & 0xFF;
    dataBuffer[3] = numericData & 0xFF;
    
    if (writeBlock(blockNumber, dataBuffer)) {
        Serial.print(" -> Wrote '");
        Serial.print(numericData);
        Serial.print("' to block ");
        Serial.println(blockNumber);
    }
}

// Core function to write a 16-byte buffer to a block
bool writeBlock(int blockNumber, byte arrayAddress[]) {
    // Authenticate the sector trailer block
    int trailerBlock = (blockNumber / 4 * 4) + 3;
    byte status = mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));

    if (status != MFRC522::STATUS_OK) {
        Serial.print("Authentication failed for block ");
        Serial.print(blockNumber);
        Serial.print(": ");
        Serial.println(mfrc522.GetStatusCodeName(status));
        return false;
    }

    // Write the data to the specified block
    status = mfrc522.MIFARE_Write(blockNumber, arrayAddress, 16);
    if (status != MFRC522::STATUS_OK) {
        Serial.print("MIFARE_Write failed for block ");
        Serial.print(blockNumber);
        Serial.print(": ");
        Serial.println(mfrc522.GetStatusCodeName(status));
        return false;
    }
    
    return true; 
