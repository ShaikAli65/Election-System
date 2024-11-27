import React, { useState } from "react";

const CandidateForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    age: "",
    gender: "",
    portfolio: null, // Initialize portfolio as null for the file
  });

  // Handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  // Handle file upload (for portfolio)
  const handleFileChange = (e) => {
    const file = e.target.files[0]; // Get the first selected file (PDF)
    setFormData({
      ...formData,
      portfolio: file,
    });
  };

  // Submit form data using FormData class
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission

    // Create a new FormData object
    const data = new FormData();
    data.append("name", formData.name);
    data.append("email", formData.email);
    data.append("age", formData.age);
    data.append("gender", formData.gender);

    if (formData.portfolio) {
      data.append("portfolio", formData.portfolio); // Append the file if selected
    }

    try {
      const response = await fetch(
        "http://election.zapto.org/admin/addCandidate",
        {
          method: "POST",
          body: data, // Send FormData object, including the file
        }
      );

      if (response.ok) {
        const result = await response.text(); // You can also use response.json() if the server responds with JSON
        alert("Form submitted successfully!");
        console.log("Response:", result);
      } else {
        alert("Failed to submit form");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error occurred while submitting form");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label>Email:</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label>Age:</label>
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={handleChange}
          required
        />
      </div>

      <div>
        <label>Gender:</label>
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          required
        >
          <option value="">Select Gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div>
        <label>Portfolio (PDF):</label>
        <input
          type="file"
          name="portfolio"
          accept="application/pdf" // Only accept PDF files
          onChange={handleFileChange}
          required
        />
      </div>

      <button type="submit" className="bg-black text-white rounded-lg">
        Submit
      </button>
    </form>
  );
};

export default CandidateForm;
