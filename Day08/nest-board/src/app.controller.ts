import { Controller, Get, Param } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}
posts = [
  {
    id: 1,
    title:'첫째 제목',
  },
  {
    id: 2,
    title:'둘째 제목',
  },
  {
    id: 3,
    title:'셋째 제목',
  }
]
@Get()
함수명(): string{
	return "아무글";
}
@Get('post/:post_id')
함수명2(@Param('post_id') post_id: string){
  const postId = Number(post_id);
  const post = this.posts.find((post) => post.id === postId);

  return post;
}


}
 