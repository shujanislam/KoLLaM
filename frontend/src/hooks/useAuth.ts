import { useEffect, useState } from "react";
import { supabase } from "../services/supabase";

type AuthUser = {
  id: string;
  email: string;
  emailVerified: boolean;
} | null;

export default function useAuth() {
  const [user, setUser] = useState<AuthUser>(null);
  const [loading, setLoading] = useState(true);

  // 🔹 Check current session on mount
  useEffect(() => {
    const getUser = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        setUser({
          id: user.id,
          email: user.email!,
          emailVerified: user.email_confirmed_at !== null,
        });
      } else {
        setUser(null);
      }
      setLoading(false);
    };

    getUser();

    // 🔹 Listen for auth state changes (login/logout/verification)
    const { data: listener } = supabase.auth.onAuthStateChange(
      async (_event, session) => {
        if (session?.user) {
          setUser({
            id: session.user.id,
            email: session.user.email!,
            emailVerified: session.user.email_confirmed_at !== null,
          });
        } else {
          setUser(null);
        }
      }
    );

    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

   
  const signUp = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signUp({ email, password });
    return { data, error };
  };
 
  const signIn = async (email: string, password: string) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    return { data, error };
  };
 
  const signOut = async () => {
    await supabase.auth.signOut();
    setUser(null);
  };

  return {
    user,
    loading,
    signUp,
    signIn,
    signOut,
  };
}
