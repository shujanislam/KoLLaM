import express from "express";
import cors from "cors";
const graphqlHTTP = require("express-graphql").graphqlHTTP;
import { connectDB } from "./config/db.config";
import { schema } from "./graphql"; // your merged typeDefs + resolvers

const app = express();

app.use(express.json());
app.use(cors({ origin: "*" }));

app.use(
  "/graphql",
  graphqlHTTP({
    schema,
    graphiql: true,
  })
);

const PORT = process.env.PORT || 8080;

(async () => {
  try {
    await connectDB();
    app.listen(PORT, () => {
      console.log(`🚀 Server running at http://localhost:${PORT}/graphql`);
    });
  } catch (err) {
    console.error("❌ Failed to connect to DB:", err);
    process.exit(1);
  }
})();
