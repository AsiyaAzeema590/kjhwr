import { useEffect, useState } from "react";

import MetricCard from "./components/MetricCard";
import ForecastChart from "./components/ForecastChart";
import ErrorChart from "./components/ErrorChart";

import { getAnalysis } from "./services/api";

import "./index.css";


function App() {
  const [analysis, setAnalysis] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);


  useEffect(() => {
    async function loadAnalysis() {
      try {
        setLoading(true);
        setError(null);

        const data = await getAnalysis();

        setAnalysis(data);
      } catch (err) {
        console.error(err);

        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadAnalysis();
  }, []);


  if (loading) {
    return (
      <div className="loading">
        <div className="loading-card">
          <h2>
            Loading wind analysis...
          </h2>

          <p>
            Fetching January 2026 Elexon data.
          </p>
        </div>
      </div>
    );
  }


  if (error) {
    return (
      <div className="error-page">
        <div className="error-card">

          <h2>
            Unable to load data
          </h2>

          <p>
            {error}
          </p>

          <p>
            Make sure the FastAPI backend
            is running on port 8000.
          </p>

        </div>
      </div>
    );
  }


  if (!analysis) {
    return null;
  }


  const metrics =
    analysis.metrics || {};

  const chartData =
    analysis.data || [];


  return (
    <div className="app">

      {/* Header */}

      <header className="header">

        <div className="header-content">

          <div>

            <p className="eyebrow">
              ENERGY PROCUREMENT ANALYTICS
            </p>

            <h1>
              UK Wind Forecast Dashboard
            </h1>

            <p className="subtitle">
              January 2026 day-ahead wind
              generation analysis
            </p>

          </div>


          <div className="status-badge">

            <span className="status-dot"></span>

            Data Loaded

          </div>

        </div>

      </header>


      {/* Main */}

      <main className="main">

        {/* Metrics */}

        <section className="section">

          <div className="section-heading">

            <h2>
              Forecast Accuracy
            </h2>

            <p>
              Day-ahead forecast compared
              with actual wind generation.
            </p>

          </div>


          <div className="metrics">

            <MetricCard
              title="Analysis Records"
              value={
                metrics.records || 0
              }
            />


            <MetricCard
              title="Mean Absolute Error"
              value={
                metrics.mae ?? 0
              }
              unit="MW"
            />


            <MetricCard
              title="RMSE"
              value={
                metrics.rmse ?? 0
              }
              unit="MW"
            />


            <MetricCard
              title="Forecast Bias"
              value={
                metrics.bias ?? 0
              }
              unit="MW"
            />

          </div>

        </section>


        {/* Forecast Chart */}

        <section className="panel">

          <div className="panel-header">

            <div>

              <h2>
                Forecast vs Actual
              </h2>

              <p>
                January 2026 wind generation
                in megawatts.
              </p>

            </div>

          </div>


          <ForecastChart
            data={chartData}
          />

        </section>


        {/* Error Chart */}

        <section className="panel">

          <div className="panel-header">

            <div>

              <h2>
                Forecast Error
              </h2>

              <p>
                Error = forecast − actual.
                Positive values indicate
                over-forecasting.
              </p>

            </div>

          </div>


          <ErrorChart
            data={chartData}
          />

        </section>


        {/* Business Insight */}

        <section className="insight">

          <div className="insight-icon">
            ⚡
          </div>


          <div>

            <h2>
              Procurement Decision Insight
            </h2>

            <p>
              The dashboard compares the
              day-ahead wind forecast with
              actual generation to quantify
              forecast uncertainty.
            </p>

            <p>
              A positive bias indicates
              over-forecasting, while a
              negative bias indicates
              under-forecasting.
            </p>

          </div>

        </section>


        {/* Data source */}

        <section className="data-source">

          <strong>
            Data source:
          </strong>

          <span>
            Elexon BMRS — FUELHH actual
            generation and WINDFOR wind
            forecasts.
          </span>

        </section>

      </main>

    </div>
  );
}


export default App;