import React, { useState } from "react";
import HCaptcha from "@hcaptcha/react-hcaptcha";

const RecaptchaTrial = () => {
  const [isVerified, setIsVerified] = useState(false);

  const handleVerificationSuccess = (token) => {
    console.log("CAPTCHA verified successfully!", token);
    setIsVerified(true);
  };

  return (
    <div>
      <HCaptcha
        sitekey="7cfaca32-5aa2-4bf8-a674-c7aee0cee5ee" // Replace with your hCaptcha site key
        onVerify={handleVerificationSuccess}
        size="normal" // Options: 'normal' or 'compact'
        theme="light" // Options: 'light' or 'dark'
      />
      <button
        onClick={() =>
          isVerified ? alert("Verified!") : alert("Please complete CAPTCHA")
        }
      >
        Submit
      </button>
    </div>
  );
};

export default RecaptchaTrial;
