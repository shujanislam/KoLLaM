'use client';

export default function Generate() {
  const generateKolam = async() => {
    try{
      const res = await fetch("http://localhost:8081/generate-kolam", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if(res.ok){
        const data = await res.json();

        console.log(data);
      }
    }
    catch(err){
      console.log(err.message);
    }
  }
  
  return (
  <div>
    <button onClick={generateKolam}>Generate Kolam</button>
  </div>
  );
}
