package test_package;

public class GodClass {
    
    
    int field3;

    

    int method2(){
        return this.field3;
    }

    
}

// New class(GodClassExtracted) generated by CodART
class GodClassExtracted
{
	 int field1;
	 int field2;

	int method1(){
        return this.field1 + this.field2;
    }

	int method3(){
        return this.field2 + this.field1;
    }
}
