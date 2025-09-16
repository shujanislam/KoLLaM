import {supabase} from './supabase';

export async function signInWithEmail(email: string, password: string) {
  const {data, error} = await supabase.auth.signInWithPassword({
    email,
    password,
   
  });}
  export async function signUpWithEmail(email: string, password: string) {
    const {data, error} = await supabase.auth.signUp({
      email,
      password,
       options:{
        emailRedirectTo: 'http://localhost:3000/feed',
    },
    });
    return {data, error};
  }
  export async function signOut() {
    const {error} = await supabase.auth.signOut();
    return {error};
  }
  
  export async function getCurrentUser(){ const {
    data: { user },
    error,
  } = await supabase.auth.getUser();
  if (error) throw error;
  return user;
}