import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

export const firebaseConfig = {
    apiKey: "AIzaSyC_MhhUwX49wqfPLJV7mhcEM0M_1l_zO7M",
    authDomain: "greendesign-9ed49.firebaseapp.com",
    projectId: "greendesign-9ed49",
    storageBucket: "greendesign-9ed49.appspot.com",
    messagingSenderId: "1058011484974",
    appId: "1:1058011484974:web:12d6bd288b1a463a7260bf"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
export const db = getFirestore(app);

// Initialize Auth
export const auth = getAuth(app);