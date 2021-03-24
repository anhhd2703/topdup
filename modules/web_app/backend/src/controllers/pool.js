const Pool = require("pg").Pool;

const createPool = (host, database, user, password, port=process.env.POOL_PORT) => (
  new Pool({
    user: user,
    host: host,
    database: database,
    password: password,
    port: port
  })
);

export default createPool;
