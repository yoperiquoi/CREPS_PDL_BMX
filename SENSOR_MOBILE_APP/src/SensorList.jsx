import React from "react";
import { FlatList, Pressable } from "react-native";
import { View } from "react-native";
import { StyleSheet } from "react-native";
import { Text } from "react-native";

export default function SensorList({ setSensor, data, handleSelectSensor }) {
  const Item = ({ item }) => (
    <Pressable
      onPress={() => {
        setSensor(item);
        handleSelectSensor(item);
      }}
    >
      <View style={styles.item}>
        <Text style={styles.title}>{item["F_NOM"]}</Text>
      </View>
    </Pressable>
  );

  return (
    <FlatList
      data={data}
      renderItem={({ item }) => (
        <Item item={item} keyExtractor={(item) => item["K_ID"]} />
      )}
      contentContainerStyle={styles.container}
      style={{ width: "100%", marginTop: 20 }}
    ></FlatList>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    marginTop: 20,
  },
  item: {
    backgroundColor: "#3498db",
    padding: 20,
    marginVertical: 12,
    marginHorizontal: 16,
    borderRadius: 10,
    textAlign: "center",
    width: 270,
  },
  title: {
    fontSize: 32,
    color: "#fff",
    textTransform: "capitalize",
    textAlign: "center",
    fontWeight: "bold",
  },
});
