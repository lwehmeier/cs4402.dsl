package uk.standrews.cs.cs4402.dsl;

import com.google.inject.Inject;
import com.google.inject.Injector;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.xtext.parser.IParseResult;
import org.eclipse.xtext.parser.IParser;
import org.eclipse.xtext.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;


public class Main {
    public static void main(String[] args){
        System.out.println("Hello World!!");
        Main xtp = new Main();
        try {
            EObject root = xtp.parse(new FileReader("/cs/home/lw96/IdeaProjects/cs4402.dsl/test.bcsp"));
            System.out.println(root);
        }
        catch (IOException ex){
            ex.printStackTrace();
        }
    }
    @Inject
    public IParser parser;

    public Main() {
        setupParser();
    }

    private void setupParser() {
        Injector injector = new DSLStandaloneSetup().createInjectorAndDoEMFRegistration();
        injector.injectMembers(this);
    }

    /**
     * Parses data provided by an input reader using Xtext and returns the root node of the resulting object tree.
     * @param reader Input reader
     * @return root object node
     * @throws IOException when errors occur during the parsing process
     */
    public EObject parse(Reader reader) throws IOException
    {
        IParseResult result = parser.parse(reader);
        if(result.hasSyntaxErrors())
        {
            throw new ParseException("Provided input contains syntax errors.");
        }
        return result.getRootASTElement();
    }
}
