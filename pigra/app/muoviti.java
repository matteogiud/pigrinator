
import java.io.IOException;
import javax.bluetooth.*;
import javax.microedition.io.*;


 import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class muoviti {

                public static void main(String[] args) {
                    String topic        = "esp32/sensors";
                    String broker       = "tcp://esp32.local:1883"; // sostituisci con l'indirizzo IP o hostname del tuo ESP32
                    String clientId     = "JavaClient";
                    MemoryPersistence persistence = new MemoryPersistence();

                    try {
                        // creiamo un'istanza del client MQTT e lo connettiamo al broker
                        MqttClient client = new MqttClient(broker, clientId, persistence);
                        MqttConnectOptions connOpts = new MqttConnectOptions();
                        connOpts.setCleanSession(true);
                        System.out.println("Connettendo al broker: "+broker);
                        client.connect(connOpts);
                        System.out.println("Connesso");

                        // iscriviamo il client al topic dei sensori dell'ESP32
                        System.out.println("Iscritto al topic "+topic);
                        client.subscribe(topic);

                        // definiamo un listener per ricevere i messaggi dal broker
                        client.setCallback(new MqttCallback() {
                            public void messageArrived(String topic, MqttMessage message) throws Exception {
                                // gestiamo il messaggio ricevuto dal broker
                                System.out.println("Messaggio ricevuto:");
                                System.out.println("\tTopic: "+topic);
                                System.out.println("\tMessage: "+new String(message.getPayload()));
                            }

                            public void deliveryComplete(IMqttDeliveryToken token) {
                            }

                            public void connectionLost(Throwable cause) {
                                System.out.println("Connessione persa: "+cause.getMessage());
                            }
                        });

                    } catch(MqttException me) {
                        System.out.println("Eccezione: "+me.getMessage());
                        me.printStackTrace();
                    }
                }
            }