import { StyleSheet, Text } from "react-native";
import {
  requestForegroundPermissionsAsync,
  getCurrentPositionAsync,
} from "expo-location";
import { useEffect } from "react";
import { useState } from "react";
import { Gyroscope, Accelerometer, Magnetometer } from "expo-sensors";
import io from "socket.io-client";
import { Button } from "react-native";
import { SafeAreaView } from "react-native";
import SensorList from "./src/SensorList";

/*
En l'absence de balise capteur dédiés, un téléphone est un moyen rapide d'avoir accès à la géolocalisation ainsi qu'au
gyroscope, accelerometer et magnetometer (ses derniers ne sont cependant pas précis sur des téléphone bas de gamme, genre 
  les xiaomi de l'IMT. cependant leurs GPS sont corrects donc ils sont utilisables comme balise fixe).
*/

/*
Le code ci dessous à été écrit dans le but d'avoir une preuve de concept rapide dans un contexte où l'utilisation de 
téléphone est temporaire.
Le code n'est donc pas optimisé, factorisé et plutôt moche. Merci de votre compréhension.
*/

export default function App() {
  //Les dernières données capturées
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [gyroscope, setGyroscope] = useState({ x: 0, y: 0, z: 0 });
  const [accelerometer, setAccelerometer] = useState({ x: 0, y: 0, z: 0 });
  const [magnetometer, setMagnetometer] = useState({ x: 0, y: 0, z: 0 });

  //Les abonnements au gryoscope, accelerometre et magnetometre
  const [subscriptionMagnetometer, setSubscriptionMagnetometer] =
    useState(null);
  const [subscriptionAccelerometer, setSubscriptionAccelerometer] =
    useState(null);
  const [subscription, setSubscription] = useState(null);

  //Les urls des serveurs
  const socket_url = "http://51.75.124.195:37591";
  const sensor_api_url = "http://51.75.124.195:5000/getCapteurs";

  //Si record est à true, on envoie les données au serveur
  const [record, setRecord] = useState(false);

  //Le set interval pour pouvoir l'arreter quand record est à false
  const [interval, setInt] = useState(null);

  /*La liste des capteurs que l'on recoit du serveur
  exemple: Velo 1, Velo 2, Balise de départ 1, Balise de départ 2, Balise d'arrivée 1, Balise d'arrivée 2
  permet de choisir quel capteur représente le téléphone
  */
  const [sensors, setSensors] = useState([]);

  /*
  Le capteur que matérialise le téléphone. Une balise fixe n'envoie que sa localisation.
  Les vélos en plus de leur localisation sont des capteurs qui envoient leur gyroscope, accelerometre et magnetometre.
  */
  const [sensor, setSensor] = useState(null);

  //Le socket pour envoyer les données au serveur
  const [socket, setSocket] = useState(null);

  //API state
  const [apiConnected, setApiConnected] = useState(false);

  // les coordonnées de la ligne d'arrivé pour arrêter le téléphone. Cette fonctionnalité ne fonctionne pas encore
  let arrivee = { borne_1: { lat: 0, lng: 0 }, borne_2: { lat: 0, lng: 0 } };

  //Lorsque l'utilisateur choisi un capteur, on le connecte au serveur
  const handleSelectSensor = (s) => {
    setSocket(
      io.connect(socket_url, {
        transports: ["websocket"],
        auth: { Username: s["F_NOM"].toUpperCase(), id: s["K_ID"] }, //Nombre de fois qu'il doit réessayer de se connecter
      })
    );
  };

  // setup de l'écoute sur le socket
  useEffect(() => {
    if (socket !== null) {
      socket.on("start_record", (data) => {
        arrivee = data;
        console.log("bornes de l'arrivée", arrivee);
        setRecord(true);
      });

      socket.on("end_record", () => {
        setRecord(false);
      });
    }
  }, [socket]);

  //Lorsque le serveur déclenche le record, on lance le set interval et les subscriptions
  useEffect(() => {
    //Récupére la liste des capteurs depuis le serveur. Si l'API est down l'application affiche un message d'erreur
    getSensors();

    // Demande la permission pour utiliser la géolocalisation
    (async () => {
      const { status } = await requestForegroundPermissionsAsync();
      if (status !== "granted") {
        alert("Permission to access location was denied");
      }
    })().catch((error) => {
      console.log(error);
    });

    // démarre le set interval pour récupérer la géolocalisation. La première valeur peut mettre 10 à 20 secondes à arriver.
    // je démarre la capture dans le vide dès que le téléphone est prêt. pour ne pas envoyer des null value au serveur
    setInt(
      setInterval(() => {
        getLocation();
      }, 100)
    );

    if (record) {
      _subscribe();
    } else {
      _unsubscribe();

      clearInterval(interval);
    }
  }, [record]);

  const getLocation = async () => {
    const location = await getCurrentPositionAsync();

    if (
      sensor !== null &&
      sensor["F_TYPE"] === "bike" &&
      // détection du franchissement de la ligne d'arrivée. Ne marche pas encore
      intersects(
        arrivee.borne_1.lat,
        arrivee.borne_1.lng,
        arrivee.borne_2.lat,
        arrivee.borne_2.lng,
        location.coords.latitude,
        location.coords.longitude,
        latitude,
        longitude
      )
    ) {
      setRecord(false);
      socket.emit("finish_detected", {});
      console.log("finish detected");
    }

    setLatitude(location.coords.latitude);
    setLongitude(location.coords.longitude);
  };

  const _subscribe = () => {
    Gyroscope.setUpdateInterval(100);
    setSubscription(
      Gyroscope.addListener((gyroscopeData) => {
        setGyroscope(gyroscopeData);
      })
    );
    Accelerometer.setUpdateInterval(100);
    setSubscriptionAccelerometer(
      Accelerometer.addListener((accelerometerData) => {
        setAccelerometer(accelerometerData);
      })
    );
    Magnetometer.setUpdateInterval(100);
    setSubscriptionMagnetometer(
      Magnetometer.addListener((magnetometerData) => {
        setMagnetometer(magnetometerData);
      })
    );
  };

  const getSensors = async () => {
    fetch(sensor_api_url)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.res !== undefined) {
          setSensors(data.res);
          setApiConnected(true);
        } else {
          setApiConnected(false);
        }
      })
      .catch((error) => {
        console.log(error);
        setApiConnected(false);
      });
  };

  const _unsubscribe = () => {
    subscription && subscription.remove();
    setSubscription(null);
    subscriptionAccelerometer && subscriptionAccelerometer.remove();
    setSubscriptionAccelerometer(null);
    subscriptionMagnetometer && subscriptionMagnetometer.remove();
    setSubscriptionMagnetometer(null);
  };

  useEffect(() => {
    if (sensor !== null && record) {
      const data =
        sensor["F_TYPE"] === "bike"
          ? {
              // Les vélos envoient tous les capteurs
              F_TIME: new Date(),
              K_CAPTEUR: sensor["K_ID"],
              F_LAT: latitude,
              F_LONG: longitude,
              F_GYRX: gyroscope.x,
              F_GYRY: gyroscope.y,
              F_GYRZ: gyroscope.z,
              F_ACCX: accelerometer.x,
              F_ACCY: accelerometer.y,
              F_ACCZ: accelerometer.z,
              F_MAGX: magnetometer.x,
              F_MAGY: magnetometer.y,
              F_MAGZ: magnetometer.z,
            }
          : {
              // les balises fixes envoient uniquement les capteurs de position
              F_TIME: new Date(),
              K_CAPTEUR: sensor["K_ID"],
              F_LAT: latitude,
              F_LONG: longitude,
            };
      postData(data);
    }
  }),
    [latitude, longitude];

  const postData = async (data) => {
    if (record) {
      // on envoie les données au serveur
      socket.emit("sensor_record", data);
    }

    return;
  };

  return (
    <SafeAreaView style={styles.container}>
      {
        //Si l'API n'est pas connectée, on affiche un message d'erreur
        !apiConnected ? (
          <Text style={styles.txt}>Waiting API</Text>
        ) : (
          <>
            {
              //Si aucun capteur n'est choisi on affiche la liste de tous les capteurs
              sensor === null ? (
                <SensorList
                  setSensor={setSensor}
                  data={sensors}
                  handleSelectSensor={handleSelectSensor}
                />
              ) : (
                //Sinon on affiche le nom du capteur et l'état de la capture
                <>
                  <Text style={{ ...styles.txt, marginBottom: 50 }}>
                    {sensor["F_NOM"]}
                  </Text>
                  {record ? (
                    <Text
                      style={{
                        ...styles.state,
                        color: "green",
                      }}
                    >
                      On
                    </Text>
                  ) : (
                    <Text
                      style={{
                        ...styles.state,
                        color: "red",
                      }}
                    >
                      Off
                    </Text>
                  )}

                  {/*Décommenter le code ci dessous pour afficher les boutons start et stop
                pour forcer le démarrage et la fin de la capture
                dans le but de tester l'envoi des données au serveur
                */
                  /* <Button
                  title="Start"
                  onPress={() => {
                    setRecord(true);
                  }}
                />
                <Button
                  title="Stop"
                  onPress={() => {
                    setRecord(false);
                    socket.emit("finish_detected", {});
                  }}
                /> */}
                  <Button
                    onPress={() => {
                      setSensor(null);
                      setRecord(false);
                      if (socket != null) {
                        socket.disconnect();
                      }
                    }}
                    title="Réinitialiser"
                    style={{ marginTop: 40 }}
                  />
                </>
              )
            }
          </>
        )
      }
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  txt: {
    fontSize: 50,
    fontWeight: "bold",
  },
  state: {
    marginBottom: 40,
    fontSize: 35,
    textTransform: "uppercase",
    fontWeight: "bold",
  },
});

// returns true if the line from (a,b)->(c,d) intersects with (p,q)->(r,s)
function intersects(a, b, c, d, p, q, r, s) {
  var det, gamma, lambda;
  det = (c - a) * (s - q) - (r - p) * (d - b);
  if (det === 0) {
    return false;
  } else {
    lambda = ((s - q) * (r - a) + (p - r) * (s - b)) / det;
    gamma = ((b - d) * (r - a) + (c - a) * (s - b)) / det;
    return 0 < lambda && lambda < 1 && 0 < gamma && gamma < 1;
  }
}
