const express = require('express');
const { ApolloServer, gql } = require('apollo-server-express');

// Define your type definitions (schema)
const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    posts: [Post]
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User
  }

  type Query {
    hello: String
    user(id: ID!): User
    users: [User]
    post(id: ID!): Post
    posts(filter: String, limit: Int, offset: Int): [Post]
  }
`;

const resolvers = {
  Query: {
    hello: () => 'Hello world!',
    user: (parent, args) => users.find(user => user.id === args.id),
    users: () => users,
    post: (parent, args) => posts.find(post => post.id === args.id),
    posts: (parent, args) => {
      let filteredPosts = posts;
      if (args.filter) {
        filteredPosts = filteredPosts.filter(post =>
          post.title.toLowerCase().includes(args.filter.toLowerCase())
        );
      }
      if (args.offset !== undefined) {
        filteredPosts = filteredPosts.slice(args.offset);
      }
      if (args.limit !== undefined) {
        filteredPosts = filteredPosts.slice(0, args.limit);
      }
      return filteredPosts;
    },
  },
  User: {
    posts: (parent) => posts.filter(post => post.authorId === parent.id),
  },
  Post: {
    author: (parent) => users.find(user => user.id === parent.authorId),
  },
};

const users = [
  { id: '1', name: 'John Doe', email: 'john@example.com' },
  { id: '2', name: 'Jane Doe', email: 'jane@example.com' },
];

const posts = [
  { id: '1', title: 'GraphQL is Awesome', content: 'GraphQL is great for APIs', authorId: '1' },
  { id: '2', title: 'Introduction to GraphQL', content: 'GraphQL basics', authorId: '1' },
  { id: '3', title: 'Advanced GraphQL', content: 'Deep dive into GraphQL', authorId: '2' },
];

// Create an Apollo server
const server = new ApolloServer({ typeDefs, resolvers });

// Initialize the app
const app = express();

// Apply the Apollo GraphQL middleware and set the path to /api
server.start().then(() => {
  server.applyMiddleware({ app, path: '/api' });

  // Start the server
  app.listen({ port: 4000 }, () =>
    console.log(`🚀 Server ready at http://localhost:4000${server.graphqlPath}`)
  );
});
