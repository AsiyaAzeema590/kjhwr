import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

function ForecastChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="empty-chart">
        No forecast data available.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart
        data={data}
        margin={{
          top: 10,
          right: 20,
          left: 10,
          bottom: 10,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="time"
          tick={{ fontSize: 11 }}
        />

        <YAxis
          label={{
            value: "MW",
            angle: -90,
            position: "insideLeft",
          }}
        />

        <Tooltip />

        <Legend />

        <Line
          type="monotone"
          dataKey="forecast"
          name="Forecast"
          dot={false}
          strokeWidth={2}
        />

        <Line
          type="monotone"
          dataKey="actual"
          name="Actual"
          dot={false}
          strokeWidth={2}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export default ForecastChart;
