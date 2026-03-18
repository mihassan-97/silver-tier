export default function Home() {
  return (
    <main style={{
      fontFamily: 'system-ui, sans-serif',
      padding: '4rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      maxWidth: 640,
      margin: '0 auto'
    }}>
      <h1>Silver Tier AI Employee</h1>
      <p>This is a simple Next.js frontend placeholder.</p>
      <p>
        The backend API endpoints live in <code>/api</code>. Use them for tasks, approvals,
        and agent automation.
      </p>
    </main>
  );
}
