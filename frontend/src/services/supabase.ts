import { createClient } from '@supabase/supabase-js';

// These will be replaced with your actual values at the end
const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://osdvdaqqiacbprlcykmj.supabase.co';
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9zZHZkYXFxaWFjYnBybGN5a21qIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc4NDIzNzUsImV4cCI6MjA3MzQxODM3NX0.wDu21kbzJr49r9OrOcu5QreWEr3cVXvUpRXJ6_Bvxe0';

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
