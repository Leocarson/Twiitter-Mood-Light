byte Red = 6;
byte Blue = 9;
byte Green = 3;
void setup() {
  // put your setup code here, to run once:
  pinMode(Red,OUTPUT);
  pinMode(Blue,OUTPUT);
  pinMode(Green,OUTPUT);
  Serial.begin(9600);
  analogWrite(Red,0);
  analogWrite(Blue,0);
  analogWrite(Green,0);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    String string = Serial.readStringUntil('\n');

    int comma1 = string.indexOf(',');
    int comma2 = string.indexOf(',',comma1 + 1);

    String first = string.substring(0,comma1);
    String second = string.substring(comma1 + 1,comma2);
    String third = string.substring(comma2 + 1);

    int r = first.toInt();
    int g = second.toInt();
    int b = third.toInt();
    
    
    analogWrite(Red,r);
    analogWrite(Green,g);
    analogWrite(Blue,b);
  }
}
