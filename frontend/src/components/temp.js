import React, { useState } from "react";

const UserForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    age: "",
    gender: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(formData);

    try {
      const response = await fetch(
        "http://election.zapto.org/admin/addCandidate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        }
      );

      if (response.ok) {
        const result = await response.json();
        alert("User added successfully: " + JSON.stringify(result));
      } else {
        alert("Failed to add user");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error occurred while sending data");
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
          className="border border-gray-300 rounded-md p-2"
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
          className="border border-gray-300 rounded-md p-2"
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
          className="border border-gray-300 rounded-md p-2"
          required
        />
      </div>

      <div>
        <label>Gender:</label>
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
          className="border border-gray-300 rounded-md p-2"
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
      <button type="submit" className="bg-black text-white">
        Submit
      </button>
    </form>
  );
};

export default UserForm;
