// AC済み問題: abc373_b
// 提出日時: 2024-10-21 16:07:45
// 実行時間: 69ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC373;

import java.util.*;
public class B{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        String[] keybord = {"A","B","C","D","E","F","G","H",
                           "I","J","K","L","M","N","O","P",
                           "Q","R","S","T","U","V","W","X","Y","Z"};
        int precount = 0;
        int count = 0;
        int currentIndex = s.indexOf("A");
        int nextIndex = 0;  
        
        for(int i = 1 ; i < 26 ; i++){
          
          precount = 0;
          
          nextIndex = s.indexOf(keybord[i]);
          precount = Math.abs(nextIndex - currentIndex);
          count += precount;
          currentIndex = nextIndex;
        }
        System.out.println(count);
    }
}