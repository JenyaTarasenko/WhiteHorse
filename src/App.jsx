import { useState } from 'react'
import './App.css';
import RegisterForm from './components/RegisterForm/RegisterForm';
import DomainScanner from './components/DomenScan/DomenScan';

function App() {
  const [isRegistered, setIsRegistered] = useState(false);
 
  return (
    <>
      {!isRegistered ? (
          <RegisterForm onSuccess={() => setIsRegistered(true)} />
        ) : (
        <DomainScanner />
      )}
    </>
  );
}

export default App
