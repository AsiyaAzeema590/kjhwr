function MetricCard({ title, value, unit }) {
  return (
    <div className="metric-card">
      <p className="metric-title">{title}</p>

      <div className="metric-value">
        {value}
      </div>

      {unit && (
        <span className="metric-unit">
          {unit}
        </span>
      )}
    </div>
  );
}

export default MetricCard;