#include <esp_now.h>
#include <WiFi.h>

#define MESSAGE_SIZE 50

class EspNowCommunication
{
private:
    uint8_t peerAddress[6];   // MAC address del peer
    bool initialized = false; // Flag per verificare se l'ESP-NOW è stato inizializzato

    // Buffer per i messaggi in entrata e in uscita
    uint8_t incomingMessage[MESSAGE_SIZE];
    uint8_t outgoingMessage[MESSAGE_SIZE];

    // Callback per la ricezione dei dati
    static void onDataReceived(const uint8_t *peerMacAddress, const uint8_t *data, int dataLength)
    {
        // Cast dell'oggetto di questa classe per chiamare il metodo onDataReceived non statico
        EspNowCommunication *communication = (EspNowCommunication *)esp_now_get_peeresp_now_get_peer_extra(peerMacAddress);

        // Copia i dati ricevuti nel buffer
        memcpy(communication->incomingMessage, data, dataLength);
    }

public:
    // Costruttore, riceve il MAC address del peer con cui comunicare
    EspNowCommunication(uint8_t address[6])
    {
        memcpy(peerAddress, address, sizeof(peerAddress));
    }

    // Metodo per inizializzare l'ESP-NOW
    bool init()
    {
        if (!initialized)
        {
            if (esp_now_init() == ESP_OK)
            {
                // Registra il peer
                esp_now_peer_info_t peerInfo;
                memcpy(peerInfo.peer_addr, peerAddress, sizeof(peerAddress));
                peerInfo.channel = 0;
                peerInfo.encrypt = false;

                // Aggiungi il peer
                if (esp_now_add_peer(&peerInfo) == ESP_OK)
                {
                    // Salva il puntatore all'oggetto di questa classe nella struttura peer_extra
                    esp_now_set_peer_extra(peerAddress, this);

                    // Registra il callback per la ricezione dei dati
                    esp_now_register_recv_cb(onDataReceived);

                    initialized = true;
                }
            }
        }
        return initialized;
    }

    // Metodo per inviare un messaggio
    bool send(const uint8_t *message, int length)
    {
        if (esp_now_send(peerAddress, message, length) == ESP_OK)
        {
            // Copia il messaggio nel buffer di output
            memcpy(outgoingMessage, message, length);
            return true;
        }
        return false;
    }

    // Metodo per verificare se ci sono messaggi in entrata
    bool available()
    {
        return esp_now_is_peer_exist(peerAddress) && esp_now_recv_peer(peerAddress, incomingMessage, MESSAGE_SIZE, 0) > 0;
    }

    // Metodo per leggere un messaggio in entrata
    int read(uint8_t *buffer, int length)
    {
        int len = esp_now_recv_peer(peerAddress, buffer, length, 0);
        return len > 0 ? len : 0;
    }

    // Metodo per leggere l'ultimo messaggio in uscita
    void getLastOutgoingMessage(uint8_t *buffer, int length)
    {
        memcpy(buffer, outgoingMessage, length);
    }

    // Metodo per leggere l'ultimo messaggio in entrata
    void getLastIncomingMessage(uint8_t *buffer, int length)
    {
        memcpy(buffer, incomingMessage, length);
    }
};