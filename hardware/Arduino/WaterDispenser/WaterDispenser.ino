#include <EEPROM.h>

// ============================================================
// Identification appareil
// ============================================================

const char DEVICE_NAME[] = "TB-Microscope-Water-Dispenser-V1";

// ============================================================
// Brochage
// ============================================================

const uint8_t PIN_STEP = 6;
const uint8_t PIN_DIR  = 5;
const uint8_t PIN_EN   = 7;
const uint8_t ledPin   = 13;


// ============================================================
// Limites mécaniques
// En micro-pas
// ============================================================

const long MOTOR_MIN_POSITION = 0;
const long MOTOR_MAX_POSITION = 252000;


// ============================================================
// EEPROM
// ============================================================

const int EEPROM_POSITION_ADDR = 0;


// ============================================================
// Etat moteur
// ============================================================

enum MotorMode {
    MOTOR_IDLE,
    MOTOR_MOVE,
    MOTOR_CONTINUOUS,
    MOTOR_CRAWL
};

MotorMode motorMode = MOTOR_IDLE;

long motorPosition = 0;
long targetPosition = 0;

int motorDirection = 1;  // +1 ou -1

unsigned long stepIntervalUs = 1000;
unsigned long lastStepUs = 0;


// ============================================================
// Initialisation
// ============================================================

void setup() {

    pinMode(PIN_STEP, OUTPUT);
    pinMode(PIN_DIR, OUTPUT);
    pinMode(PIN_EN, OUTPUT);
    pinMode(ledPin, OUTPUT);

    deactivateMotor();

    Serial.begin(115200);

    loadMotorPosition();

    Serial.println("STATUS READY");
}


// ============================================================
// Boucle principale
// ============================================================

void loop() {

    readSerial();
    updateMotor();
}


// ============================================================
// EEPROM
// ============================================================

void loadMotorPosition() {

    EEPROM.get(EEPROM_POSITION_ADDR, motorPosition);

    // Protection minimale contre une EEPROM non initialisée
    if (motorPosition < MOTOR_MIN_POSITION ||
        motorPosition > MOTOR_MAX_POSITION) {

        motorPosition = MOTOR_MIN_POSITION;
    }
}


void saveMotorPosition() {

    EEPROM.put(EEPROM_POSITION_ADDR, motorPosition);
}


// ============================================================
// Activation moteur
// ============================================================

void activateMotor() {

    // À inverser si ton driver utilise une autre logique
    digitalWrite(PIN_EN, LOW);
}


void deactivateMotor() {

    digitalWrite(PIN_EN, HIGH);
}


// ============================================================
// Génération d'un pas
// ============================================================

void doStep() {

    digitalWrite(PIN_STEP, HIGH);
    delayMicroseconds(3);
    digitalWrite(PIN_STEP, LOW);

    motorPosition += motorDirection;
}


// ============================================================
// Service moteur NON BLOQUANT
// ============================================================

void updateMotor() {

    if (motorMode == MOTOR_IDLE) {
        return;
    }

    unsigned long now = micros();

    if ((unsigned long)(now - lastStepUs) < stepIntervalUs) {
        return;
    }

    lastStepUs = now;


    // --------------------------------------------------------
    // Protection limites logicielles
    // --------------------------------------------------------

    if (motorDirection > 0 &&
        motorPosition >= MOTOR_MAX_POSITION) {

        stopMotor();
        return;
    }

    if (motorDirection < 0 &&
        motorPosition <= MOTOR_MIN_POSITION) {

        stopMotor();
        return;
    }


    // --------------------------------------------------------
    // Mouvement vers une position cible
    // --------------------------------------------------------

    if (motorMode == MOTOR_MOVE) {

        if (motorPosition == targetPosition) {

            stopMotor();
            return;
        }

        doStep();

        if (motorPosition == targetPosition) {

            stopMotor();
        }

        return;
    }


    // --------------------------------------------------------
    // Mouvement continu
    // --------------------------------------------------------

    if (motorMode == MOTOR_CONTINUOUS ||
        motorMode == MOTOR_CRAWL) {

        doStep();
    }
}


// ============================================================
// Mouvement d'un nombre déterminé de pas
// ============================================================

bool startMove(
    long steps,
    unsigned long stepsPerSecond,
    uint8_t dir
) {

    if (steps <= 0 || stepsPerSecond == 0) {
        return false;
    }

    motorDirection = dir ? -1 : 1;

    long requestedTarget =
        motorPosition + motorDirection * steps;


    // Refus plutôt que clamp silencieux
    if (requestedTarget < MOTOR_MIN_POSITION ||
        requestedTarget > MOTOR_MAX_POSITION) {

        return false;
    }

    targetPosition = requestedTarget;

    stepIntervalUs = 1000000UL / stepsPerSecond;

    digitalWrite(
        PIN_DIR,
        motorDirection > 0 ? LOW : HIGH
    );

    activateMotor();

    motorMode = MOTOR_MOVE;

    lastStepUs = micros();

    return true;
}


// ============================================================
// Mouvement continu
// ============================================================

bool startContinuousMove(
    unsigned long stepsPerSecond,
    uint8_t dir
) {

    if (stepsPerSecond == 0) {
        return false;
    }

    motorDirection = dir ? -1 : 1;

    stepIntervalUs = 1000000UL / stepsPerSecond;

    digitalWrite(
        PIN_DIR,
        motorDirection > 0 ? LOW : HIGH
    );

    activateMotor();

    motorMode = MOTOR_CONTINUOUS;

    lastStepUs = micros();

    return true;
}

// ============================================================
// Mouvement Crawl
// ============================================================

bool startCrawlMove(unsigned long intervalMs, uint8_t dir) {

    if (intervalMs == 0) {
        return false;
    }

    // Protection contre le dépassement lors de la conversion ms -> us.
    if (intervalMs > 4294967UL) {
        return false;
    }

    motorDirection = dir ? -1 : 1;

    stepIntervalUs = intervalMs * 1000UL;

    digitalWrite(
        PIN_DIR,
        motorDirection > 0 ? LOW : HIGH
    );

    activateMotor();

    motorMode = MOTOR_CRAWL;
    lastStepUs = micros();

    return true;
}

// ============================================================
// Arrêt
// ============================================================

void stopMotor() {

    if (motorMode == MOTOR_IDLE) {
        return;
    }

    motorMode = MOTOR_IDLE;

    deactivateMotor();

    saveMotorPosition();
}


// ============================================================
// LED
// ============================================================

void blinkLED(int nb_clignotements, int delai_ms) {

    for (int i = 0; i < nb_clignotements; i++) {

        digitalWrite(ledPin, HIGH);
        delay(delai_ms);

        digitalWrite(ledPin, LOW);
        delay(delai_ms);
    }
}


// ============================================================
// MOTION STATUS
// ============================================================

void printMotion() {

    if (motorMode == MOTOR_MOVE) {
        Serial.print("MOTION MOVE ");
        Serial.print(targetPosition);
        Serial.print(" ");
        Serial.print(1000000UL / stepIntervalUs);
        Serial.print(" ");
        Serial.println(motorDirection < 0 ? 1 : 0);
    }

    else if (motorMode == MOTOR_CONTINUOUS) {
        Serial.print("MOTION RUN ");
        Serial.print(1000000UL / stepIntervalUs);
        Serial.print(" ");
        Serial.println(motorDirection < 0 ? 1 : 0);
    }

    else if (motorMode == MOTOR_CRAWL) {
        Serial.print("MOTION CRAWL ");
        Serial.print(stepIntervalUs);
        Serial.print(" ");
        Serial.println(motorDirection < 0 ? 1 : 0);
    }
    

    else {
        Serial.println("MOTION STOP");
    }
}

// ============================================================
// Lecture série
// ============================================================

void readSerial() {

    static char buffer[64];
    static uint8_t index = 0;

    while (Serial.available()) {

        char c = Serial.read();

        if (c == '\n' || c == '\r') {

            if (index > 0) {

                buffer[index] = '\0';

                processCommand(buffer);

                index = 0;
            }
        }
        else if (index < sizeof(buffer) - 1) {

            buffer[index++] = c;
        }
    }
}


// ============================================================
// Commandes
// ============================================================

void processCommand(char* command) {

    char* token;
    char* cmd = strtok(command, " ");

    if (cmd == NULL) {
        return;
    }


    // --------------------------------------------------------
    // LED
    // led 5 100
    // --------------------------------------------------------

    if (strcmp(cmd, "led") == 0) {

        token = strtok(NULL, " ");

        if (token == NULL) {
            Serial.println("ERROR LED INVALID-ARGUMENT");
            return;
        }

        int nb = atoi(token);

        token = strtok(NULL, " ");

        if (token == NULL) {
            Serial.println("ERROR LED INVALID-ARGUMENT");
            return;
        }

        int delayMs = atoi(token);

        Serial.println("LED BLINKING");
        blinkLED(nb, delayMs);

        
    }

    // --------------------------------------------------------
    // WHO
    // Retourne l'identifiant de l'appareil
    // --------------------------------------------------------

    else if (strcmp(cmd, "who") == 0) {

        Serial.println(DEVICE_NAME);
    }


    // --------------------------------------------------------
    // MOVE
    //
    // move <steps> <steps/s> <dir>
    //
    // Exemple :
    // move 2000 500 0
    // --------------------------------------------------------

    else if (strcmp(cmd, "move") == 0) {

        token = strtok(NULL, " ");

        if (token == NULL) {
            Serial.println("ERROR MOVE INVALID_ARGUMENT");
            return;
        }

        long steps = atol(token);


        token = strtok(NULL, " ");

        unsigned long speed =
            token ? atol(token) : 500;


        token = strtok(NULL, " ");

        uint8_t dir =
            token ? atoi(token) : 0;


        if (startMove(steps, speed, dir)) {

            Serial.println("MOVE STARTED");
        }
        else {

            Serial.println("ERROR MOVE INVALID_ARGUMENT");
        }
    }


    // --------------------------------------------------------
    // RUN
    //
    // Mouvement continu :
    //
    // run <steps/s> <dir>
    //
    // Exemple :
    // run 50 0
    // --------------------------------------------------------

    else if (strcmp(cmd, "run") == 0) {

        token = strtok(NULL, " ");

        if (token == NULL) {
            Serial.println("ERROR RUN INVALID_ARGUMENT");
            return;
        }

        unsigned long speed = atol(token);


        token = strtok(NULL, " ");

        uint8_t dir =
            token ? atoi(token) : 0;


        if (startContinuousMove(speed, dir)) {

            Serial.println("RUN STARTED");
        }
        else {

            Serial.println("ERROR RUN INVALID_ARGUMENT");
        }
    }

    // --------------------------------------------------------
    // CRAWL
    //
    // Mouvement continu a interval donné :
    //
    // run <ms/step> <dir>
    //
    // Exemple :
    // run 2000 0
    // --------------------------------------------------------

    else if (strcmp(cmd, "crawl") == 0) {

    token = strtok(NULL, " ");

    if (token == NULL) {
        Serial.println("ERROR CRAWL INVALID_ARGUMENT");
        return;
    }

    unsigned long intervalMs = atol(token);

    token = strtok(NULL, " ");

    uint8_t dir = token ? atoi(token) : 0;

    if (startCrawlMove(intervalMs, dir)) {
        Serial.println("CRAWL STARTED");
    }
    else {
        Serial.println("ERROR CRAWL INVALID_ARGUMENT");
    }
}


    // --------------------------------------------------------
    // STOP
    // --------------------------------------------------------

    else if (strcmp(cmd, "stop") == 0) {

        stopMotor();

        Serial.print("STOP DONE ");
        Serial.println(motorPosition);
    }


    // --------------------------------------------------------
    // POSITION
    // --------------------------------------------------------

    else if (strcmp(cmd, "pos") == 0) {
        Serial.print("POS ");
        Serial.println(motorPosition);
    }

    else if (strcmp(cmd, "motion") == 0) {
    printMotion();
    }


    else {

        Serial.println("ERROR UNKNOWN_COMMAND");
    }
    
}