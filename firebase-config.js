const firebaseConfig = {
  apiKey: "AIzaSyD_Re5Wc6Qfv6QfwDhKmkbw3zsFT5TeNNo",
  authDomain: "lory-fitness-app.firebaseapp.com",
  projectId: "lory-fitness-app",
  storageBucket: "lory-fitness-app.firebasestorage.app",
  messagingSenderId: "620087669910",
  appId: "1:620087669910:web:5d43c87a63dc08dff0feb7",
  measurementId: "G-1VNN6SE838"
};

firebase.initializeApp(firebaseConfig);

const auth = firebase.auth();
const db = firebase.firestore();
