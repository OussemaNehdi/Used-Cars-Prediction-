'use client';

import { useState } from 'react';

interface CarData {
  year: number;
  brand: string;
  model: string;
  mileage: number;
  cv: number;
  fuel_type: string;
  transmission: string;
}

interface PredictionResponse {
  predicted_price: number;
  input_data: CarData;
}

export default function Home() {
  const [formData, setFormData] = useState<CarData>({
    year: 2020,
    brand: '',
    model: '',
    mileage: 0,
    cv: 0,
    fuel_type: 'Essence',
    transmission: 'Manuelle'
  });

  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'year' || name === 'mileage' || name === 'cv' 
        ? parseInt(value) || 0 
        : value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: PredictionResponse = await response.json();
      setPrediction(data.predicted_price);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🚗 Tunisian Car Price Predictor
          </h1>
          <p className="text-lg text-gray-600">
            Get an accurate price prediction for your car based on market data
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Year */}
              <div>
                <label htmlFor="year" className="block text-sm font-medium text-gray-700 mb-2">
                  Year *
                </label>
                <input
                  type="number"
                  id="year"
                  name="year"
                  min="1990"
                  max="2025"
                  value={formData.year}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Mileage */}
              <div>
                <label htmlFor="mileage" className="block text-sm font-medium text-gray-700 mb-2">
                  Mileage (km) *
                </label>
                <input
                  type="number"
                  id="mileage"
                  name="mileage"
                  min="0"
                  value={formData.mileage}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Brand */}
              <div>
                <label htmlFor="brand" className="block text-sm font-medium text-gray-700 mb-2">
                  Brand *
                </label>
                <input
                  type="text"
                  id="brand"
                  name="brand"
                  value={formData.brand}
                  onChange={handleInputChange}
                  placeholder="e.g., Toyota, Mercedes, BMW"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Model */}
              <div>
                <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-2">
                  Model *
                </label>
                <input
                  type="text"
                  id="model"
                  name="model"
                  value={formData.model}
                  onChange={handleInputChange}
                  placeholder="e.g., Corolla, Classe A, X5"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                />
              </div>

              {/* CV (Horsepower) */}
              <div>
                <label htmlFor="cv" className="block text-sm font-medium text-gray-700 mb-2">
                  CV (Horsepower) *
                </label>
                <input
                  type="number"
                  id="cv"
                  name="cv"
                  min="1"
                  max="50"
                  value={formData.cv}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Fuel Type */}
              <div>
                <label htmlFor="fuel_type" className="block text-sm font-medium text-gray-700 mb-2">
                  Fuel Type *
                </label>
                <select
                  id="fuel_type"
                  name="fuel_type"
                  value={formData.fuel_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                >
                  <option value="Essence">Essence (Gasoline)</option>
                  <option value="Diesel">Diesel</option>
                  <option value="Hybrid">Hybrid</option>
                </select>
              </div>

              {/* Transmission */}
              <div className="md:col-span-2">
                <label htmlFor="transmission" className="block text-sm font-medium text-gray-700 mb-2">
                  Transmission *
                </label>
                <select
                  id="transmission"
                  name="transmission"
                  value={formData.transmission}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  required
                >
                  <option value="Manuelle">Manual</option>
                  <option value="Automatique">Automatic</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-3"></div>
                  Predicting...
                </div>
              ) : (
                'Get Price Prediction'
              )}
            </button>
          </form>

          {/* Results */}
          {prediction !== null && (
            <div className="mt-8 p-6 bg-green-50 border border-green-200 rounded-lg">
              <h3 className="text-lg font-semibold text-green-800 mb-2">
                💰 Predicted Price
              </h3>
              <p className="text-3xl font-bold text-green-700">
                {prediction.toLocaleString()} DT
              </p>
              <p className="text-sm text-green-600 mt-2">
                This prediction is based on current market trends and similar vehicles.
              </p>
            </div>
          )}

          {error && (
            <div className="mt-8 p-6 bg-red-50 border border-red-200 rounded-lg">
              <h3 className="text-lg font-semibold text-red-800 mb-2">
                ❌ Error
              </h3>
              <p className="text-red-700">
                {error}
              </p>
              <p className="text-sm text-red-600 mt-2">
                Make sure the FastAPI backend is running on http://localhost:8000
              </p>
            </div>
          )}
        </div>

        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Powered by AI • Built with Next.js & FastAPI</p>
        </div>
      </div>
    </div>
  );
}