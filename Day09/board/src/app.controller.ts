import { Controller, Get, Param } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}
  posts = [
{
  id:1,
  content:"1번게시글",
},
{
  id:2,
  content:"2번게시글",
}
]


  @Get()
  getHello(): string {
    return "리를 게시판에 오신걸 환영합니다.";
  }
  @Get('posts')
  postList(){
    return this.posts;
  }
  @Get('post/:post_id')
detail(@Param('post_id') post_id: string){
const postId = Number(post_id);
const post = this.posts.find((post) => post.id === postId);
if(!post){
  return "해당 글은 없습니다!";
}
return post;
}
}
