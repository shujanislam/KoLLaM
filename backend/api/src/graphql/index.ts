import path from "path";
import { loadFilesSync } from "@graphql-tools/load-files";
import { mergeTypeDefs } from "@graphql-tools/merge";
import { makeExecutableSchema } from "@graphql-tools/schema";
import { resolvers } from "./resolvers/resolver"; // your resolvers file

// Load all .graphql SDL files in this folder (typeDefs)
const typesArray = loadFilesSync(path.join(__dirname, "./typeDefs/*.graphql"));

// Merge all typeDefs into one
const typeDefs = mergeTypeDefs(typesArray);

// Create executable schema
export const schema = makeExecutableSchema({
  typeDefs,
  resolvers,
});
