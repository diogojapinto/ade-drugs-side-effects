JFLAGS = -d ./out/
JC = javac

default :
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/ArticleLanguage.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/CitationSubset.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/GeneSymbol.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/MedlineCitation.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/OtherAbstract.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/ArticlePublicationType.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/CommentsCorrections.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/Grant.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/MedlineParser.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/OtherID.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/Author.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/DataBank.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/Investigator.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/MeshHeading.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/PersonalNameSubject.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/Chemical.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/GeneralNote.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/Keyword.java
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/MeshHeadingQualifier.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/medline/SpaceFlightMission.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/GenericXMLParser.java 
		$(JC) $(JFLAGS) ./biotextEngine/xmlparsers/NodeHandler.java 
		$(JC) $(JFLAGS) ./biotextEngine/util/BioTextDBConnection.java
		jar cfm MedlineParser.jar manifest.txt -C out .

clean:
		rm /out/*