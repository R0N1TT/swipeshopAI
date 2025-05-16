// SwipeShop AI MVP Code (React Native + Banuba SDK Integration)

import React, { useState, useEffect } from 'react';
import { View, Text, Image, TouchableOpacity, FlatList, SafeAreaView, StyleSheet } from 'react-native';
import { Video } from 'expo-av';
import { Ionicons } from '@expo/vector-icons';

// Dummy Product Feed
const products = [
  {
    id: '1',
    video: 'https://example.com/video1.mp4',
    thumbnail: 'https://example.com/thumbnail1.jpg',
    brand: 'Brand A',
    name: 'Trendy Jacket',
    link: 'https://shop.com/product1',
  },
  {
    id: '2',
    video: 'https://example.com/video2.mp4',
    thumbnail: 'https://example.com/thumbnail2.jpg',
    brand: 'Brand B',
    name: 'Cool Hoodie',
    link: 'https://shop.com/product2',
  },
];

export default function App() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [wishlist, setWishlist] = useState([]);

  const handleSwipeRight = () => {
    const product = products[currentIndex];
    setWishlist([...wishlist, product]);
    setCurrentIndex((prev) => (prev + 1) % products.length);
  };

  const handleSwipeLeft = () => {
    setCurrentIndex((prev) => (prev + 1) % products.length);
  };

  const handleTryOn = () => {
    // Replace with Banuba try-on SDK integration
    alert('Launching Virtual Try-On (Banuba SDK)');
  };

  const product = products[currentIndex];

  return (
    <SafeAreaView style={styles.container}>
      <Video
        source={{ uri: product.video }}
        rate={1.0}
        volume={1.0}
        isMuted={false}
        resizeMode="cover"
        shouldPlay
        isLooping
        style={styles.video}
      />
      <View style={styles.overlay}>
        <Text style={styles.brand}>{product.brand}</Text>
        <Text style={styles.name}>{product.name}</Text>
        <View style={styles.buttons}>
          <TouchableOpacity onPress={handleSwipeLeft} style={styles.button}>
            <Ionicons name="close" size={32} color="white" />
          </TouchableOpacity>
          <TouchableOpacity onPress={handleTryOn} style={styles.button}>
            <Ionicons name="eyedrop" size={32} color="white" />
          </TouchableOpacity>
          <TouchableOpacity onPress={handleSwipeRight} style={styles.button}>
            <Ionicons name="heart" size={32} color="white" />
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  video: {
    flex: 1,
  },
  overlay: {
    position: 'absolute',
    bottom: 60,
    width: '100%',
    alignItems: 'center',
  },
  brand: {
    fontSize: 20,
    color: '#fff',
    fontWeight: '600',
  },
  name: {
    fontSize: 24,
    color: '#fff',
    fontWeight: '700',
    marginVertical: 8,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    width: '80%',
    marginTop: 16,
  },
  button: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    padding: 16,
    borderRadius: 50,
  },
});