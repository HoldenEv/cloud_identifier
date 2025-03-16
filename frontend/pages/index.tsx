// import { useState, ChangeEvent, FormEvent } from 'react';

// export default function Home() {
//   const [file, setFile] = useState<File | null>(null);
//   const [result, setResult] = useState<{ predicted_class: string; confidence: number } | null>(null);
//   const [error, setError] = useState<string | null>(null);

//   const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
//     if (event.target.files && event.target.files.length > 0) {
//       setFile(event.target.files[0]);
//     }
//   };

//   const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
//     event.preventDefault();
//     setError(null);
//     setResult(null);

//     if (!file) {
//       setError('Please select a file');
//       return;
//     }

//     const formData = new FormData();
//     console.log("form data" , formData)

//     formData.append('file', file);

//     try {
//       const response = await fetch('http://127.0.0.1:5000/predict', {
//         method: 'POST',
//         body: formData,
//       });
//       const data = await response.json();
//       console.log("data", data)

//       if (!response.ok) {
//         setError(data.error || 'Something went wrong');
//       } else {
//         setResult(data);
//       }
//     } catch (err: any) {
//       setError(err.message);
//     }
//   };

//   return (
//     <div style={{ padding: '2rem' }}>
//       <h1>Cloud Classifier</h1>
//       <form onSubmit={handleSubmit}>
//         <input type="file" accept="image/*" onChange={handleFileChange} />
//         <button type="submit" style={{ marginLeft: '1rem' }}>Upload and Predict</button>
//       </form>
//       {error && <p style={{ color: 'red', marginTop: '1rem' }}>Error: {error}</p>}
//       {result && (
//         <div style={{ marginTop: '1rem' }}>
//           <h2>Prediction Result</h2>
//           <p>Predicted Class: {result.predicted_class}</p>
//           <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
//         </div>
//       )}
//     </div>
//   );
// }

import { useState, ChangeEvent, FormEvent} from 'react';
import Image from 'next/image';


export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{ predicted_class: string; confidence: number } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setResult(null);

    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.error || 'Something went wrong');
      } else {
        setResult(data);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      backgroundColor: '#f7f7f7',
      padding: '1rem'
    }}>
      <h1 style={{ marginBottom: '1.5rem' }}>Cloud Classifier</h1>
      <Image src="/public/cloud_photo.png" alt="/public/cloud_photo.png" width={72} height={16} />

      <form onSubmit={handleSubmit} style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '2rem',
        border: '1px solid #ccc',
        borderRadius: '8px',
        backgroundColor: '#fff',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
      }}>
        <input 
          type="file" 
          accept="image/*" 
          onChange={handleFileChange} 
          style={{ marginBottom: '1rem' }}
        />
        <button type="submit" style={{
          padding: '0.5rem 1.5rem',
          border: 'none',
          borderRadius: '4px',
          backgroundColor: '#0070f3',
          color: '#fff',
          cursor: 'pointer'
        }}>
          Upload and Predict
        </button>
      </form>
      {error && <p style={{ color: 'red', marginTop: '1rem' }}>Error: {error}</p>}
      {result && (
        <div style={{ marginTop: '1rem', textAlign: 'center' }}>
          <h2>Prediction Result</h2>
          <p>Predicted Class: {result.predicted_class}</p>
          <p>Confidence: {(result.confidence * 100).toFixed(2)}%</p>
        </div>
      )}
    </div>
  );
}
