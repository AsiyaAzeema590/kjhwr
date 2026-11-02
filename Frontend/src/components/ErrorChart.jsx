import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

function ErrorChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="empty-chart">
        No error data available.
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
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

        <YAxis />

        <Tooltip />

        <Bar
          dataKey="error"
          name="Forecast Error"
        />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default ErrorChart;