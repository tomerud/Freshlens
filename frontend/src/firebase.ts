import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, User } from "firebase/auth";

const firebaseConfig = {
    apiKey: "AIzaSyDkF4G73xb05z0AiIwNxlmtkan1U06hJTA",
    authDomain: "freshlens-d61dc.firebaseapp.com",
    projectId: "freshlens-d61dc",
    storageBucket: "freshlens-d61dc.firebasestorage.app",
    messagingSenderId: "187909438408",
    appId: "1:187909438408:web:46ceb85d839b57ddb1defd"
  };

  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  const provider = new GoogleAuthProvider();


  const check_if_user_already_known = async (userId: string): Promise<boolean> => {
    try {
      const response = await fetch(`/api/is_user_already_known?user_id=${encodeURIComponent(userId)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      });
  
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      return data.known || false;

    } catch (error) {
      console.error("Error checking user:", error);
      return false;
    }
  };
  

const sign_new_user_to_db = async (userId : string, userName : string | null, email: string | null) => {
  try {
    const response = await fetch('/api/sign_user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({userId, userName, email }),
    });

    if (!response.ok) {
      alert('Signup failed. Please try again.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again.');
  }
};

const handleSubmit = async (userId : string, userName : string | null, email: string | null) => {
  const user_already_known = await check_if_user_already_known(userId)

  if (!user_already_known){
    await sign_new_user_to_db(userId, userName, email)
  }
};


const signInWithGoogle = async (): Promise<User | null> => {
  try {
    const user = (await signInWithPopup(auth, provider)).user;
    handleSubmit(user.uid, user.displayName, user.email)
    return user;
  } catch (error) {
    console.error("Login Error:", error);
    return null;
  }
};

const logout = async (): Promise<void> => {
  await signOut(auth);
};

export { auth, signInWithGoogle, logout };
