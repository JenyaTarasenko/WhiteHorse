import { useState } from 'react'
import './App.css';
import RegisterForm from './components/RegisterForm/RegisterForm';
import DomainScanner from './components/DomenScan/DomenScan';
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary';

function App() {
  const [isRegistered, setIsRegistered] = useState(false);
 
  return (
    <>
      <ErrorBoundary>
        {!isRegistered ? (
            <RegisterForm onSuccess={() => setIsRegistered(true)} />
          ) : (
          <DomainScanner />
        )}
      </ErrorBoundary>
    </>
  );
}

export default App
