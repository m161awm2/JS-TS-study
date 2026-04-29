import { Controller, Get, Body, Post } from '@nestjs/common';
import { AppService } from './app.service';
import mysql from "mysql2/promise";

const DB_HOST = "localhost";
const DB_USER = "root";
const DB_PASSWORD = "Zdzdsmsm44!";
const DB_NAME = "Day10";
const db = mysql.createPool({
  host:DB_HOST,
  user:DB_USER,
  password:DB_PASSWORD,
  database:DB_NAME
});
async function init_db(){
  const tempDb = await mysql.createConnection({
    host: DB_HOST,
    user: DB_USER,
    password: DB_PASSWORD,
    database: DB_NAME
  });
  await tempDb.query(`CREATE DATABASE IF NOT EXISTS ${DB_NAME}`);
  await tempDb.end();

  await db.query(`CREATE TABLE IF NOT EXISTS posts(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nickname TEXT,
    title VARCHAR(100),
    content TEXT
    )`);
}
init_db();

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}
  @Post('api/write')
  async write(@Body() body:any){
    await db.query('INSERT INTO posts (nickname, title, content) VALUES (?,?,?)',[body.nickname,body.title,body.content]);
    return "저장됨";
  }
  @Get('posts')
  async postList() {
    const [posts] = await db.query('SELECT * FROM posts ORDER BY id DESC');
    return posts;
  }

}
