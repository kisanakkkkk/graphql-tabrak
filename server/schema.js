const { gql } = require('apollo-server-express');

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    age: Int
    friends: [User]
    posts: [Post]
  }

  type Category {
    id: ID!
    name: String!
    posts(filter: PostFilterInput, sort: PostSortInput, pagination: PaginationInput): [Post]
  }

  type Tag {
    id: ID!
    name: String!
    posts(filter: PostFilterInput, sort: PostSortInput, pagination: PaginationInput): [Post]
  }

  type Post {
    id: ID!
    title: String!
    content: String!
    author: User!
    category: Category!
    tags: [Tag]
    comments(sort: CommentSortInput, pagination: PaginationInput): [Comment]
    createdAt: String!
  }

  type Comment {
    id: ID!
    content: String!
    post: Post!
    author: User!
    replies(sort: CommentSortInput, pagination: PaginationInput): [Comment]
    createdAt: String!
  }

  input PostFilterInput {
    authorId: ID
    categoryId: ID
    tagIds: [ID]
  }

  input PostSortInput {
    field: String!
    order: String!
  }

  input CommentSortInput {
    field: String!
    order: String!
  }

  input PaginationInput {
    limit: Int
    offset: Int
  }

  type Query {
    users: [User]
    user(id: ID!): User
    posts(filter: PostFilterInput, sort: PostSortInput, pagination: PaginationInput): [Post]
    post(id: ID!): Post
    comments(sort: CommentSortInput, pagination: PaginationInput): [Comment]
    comment(id: ID!): Comment
    categories: [Category]
    category(id: ID!): Category
    tags: [Tag]
    tag(id: ID!): Tag
  }
`;

module.exports = typeDefs;
