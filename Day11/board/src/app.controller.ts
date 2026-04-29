import {
  Body,
  Controller,
  Get,
  OnModuleInit,
  Post,
  Session,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { AppService } from './app.service';
import mysql, { Pool, RowDataPacket } from 'mysql2/promise';

type UserSession = {
  nickname?: string;
};

type WriteBody = {
  title: string;
  content: string;
};

type UserBody = {
  nickname: string;
  password: string;
};

@Controller()
export class AppController implements OnModuleInit {
  private db!: Pool;

  constructor(
    private readonly appService: AppService,
    private readonly configService: ConfigService,
  ) {}

  async onModuleInit() {
    await this.initDb();
  }

  private async initDb() {
    const host = this.configService.getOrThrow<string>('DB_HOST');
    const user = this.configService.getOrThrow<string>('DB_USER');
    const password = this.configService.getOrThrow<string>('DB_PASSWORD');
    const database = this.configService.getOrThrow<string>('DB_NAME');
    const port = Number(this.configService.get<string>('DB_PORT') ?? '3306');

    if (!/^[a-zA-Z0-9_]+$/.test(database)) {
      throw new Error(
        'DB_NAME can only contain letters, numbers, and underscores.',
      );
    }

    const tempDb = await mysql.createConnection({
      host,
      port,
      user,
      password,
    });
    await tempDb.query(`CREATE DATABASE IF NOT EXISTS \`${database}\``);
    await tempDb.end();

    this.db = mysql.createPool({
      host,
      port,
      user,
      password,
      database,
    });

    await this.db.query(`CREATE TABLE IF NOT EXISTS users(
      id INT AUTO_INCREMENT PRIMARY KEY,
      nickname VARCHAR(100),
      password TEXT
    )`);
    await this.db.query(`CREATE TABLE IF NOT EXISTS posts(
      id INT AUTO_INCREMENT PRIMARY KEY,
      nickname TEXT,
      title VARCHAR(100),
      content TEXT
    )`);
  }

  @Get('api/posts')
  async home(@Session() session: UserSession) {
    const [posts] = await this.db.query<RowDataPacket[]>(
      'SELECT * FROM posts ORDER BY id DESC',
    );
    return { nickname: session.nickname, posts };
  }

  @Post('api/write')
  async write(@Body() body: WriteBody, @Session() session: UserSession) {
    if (!session.nickname) {
      return { message: '로그인을 해주세요' };
    }

    await this.db.query(
      'INSERT INTO posts (nickname,title,content) VALUES (?,?,?)',
      [session.nickname, body.title, body.content],
    );
    return { message: '글쓰기 완료' };
  }

  @Post('api/login')
  async login(@Body() body: UserBody, @Session() session: UserSession) {
    const [isLogin] = await this.db.query<RowDataPacket[]>(
      'SELECT * FROM users WHERE nickname = ? AND password = ?',
      [body.nickname, body.password],
    );

    if (isLogin.length === 0) {
      return { message: '비밀번호나 닉네임이 잘못되었습니다' };
    }

    session.nickname = body.nickname;
    return { message: '로그인 완료' };
  }

  @Post('api/signup')
  async sign(@Body() body: UserBody) {
    const [isExists] = await this.db.query<RowDataPacket[]>(
      'SELECT * FROM users WHERE nickname = ?',
      [body.nickname],
    );

    if (isExists.length !== 0) {
      return { message: '이미 존재하는 닉네임입니다' };
    }

    await this.db.query('INSERT INTO users (nickname,password) VALUES (?,?)', [
      body.nickname,
      body.password,
    ]);
    return { message: '회원가입이 완료되었습니다' };
  }
}
//