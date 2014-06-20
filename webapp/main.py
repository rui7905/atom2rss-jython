# coding: utf-8
import sys, javax, os
from java.lang import Exception, Thread, String
from java.io import StringReader, StringWriter, InputStreamReader, IOException, BufferedReader
from javax.xml.transform import Transformer, TransformerFactory, TransformerException
from javax.xml.transform.stream import StreamResult, StreamSource
from java.net import URL, MalformedURLException

def handler(environ, start_response):
    reload(sys)
    sys.setdefaultencoding('UTF8')
    welcomeString = "<html><head><title>atom2rss converter &bull; Atom to RSS2 converter</title><style>body { padding: 20px 40px; font-family: Verdana, Helvetica, Sans-Serif; font-size: medium; }</style></head><body><form method=\"post\"><h1>atom2rss converter written with Jython</h1><p>This tool will let you convert your atom 1.0 feed into an RSS2 feed that can be imported into WordPress.</p><p>Please read the full instructions before starting.</p><p><input type=\"text\" name=\"atom\" style=\"width: 400px;\"><input type=\"submit\" value=\"Convert\"></p><h2>Instructions</h2><p><strong>Step 1</strong>: Enter the url of an atom feed urls, e.g. <i>http://yoursite.com/atom.xml</i><br /></p><p><strong>Step 2</strong>: After clicking the \"Convert\" button, head to File / Save As... and save the file as rss.xml to your desktop.</p><p><strong>Step 3</strong>: Use this rss.xml file to import your data into WordPress under Import / RSS.</p><h2>About</h2><p>This tool is online as a convenience designed by <a href=\"http://kevin.9511.net/\">Kevin Li</a>.</p><p>Your can use it to import GoogleReader or Blogger data into Wordpress.</p></form></body></html>"
    response_parts = []
    header_str = ''
    if environ['REQUEST_METHOD'] == 'POST':
        post = environ['j2ee.request']
        if post.getParameterValues('atom') is None:
            bs = welcomeString
        else:
            try:
                atom = post.getParameterValues('atom')[0]
                
                atomUrl = URL(str(atom))
                atomSource = StreamSource(InputStreamReader(atomUrl.openStream(), "utf-8"))

                file = open(os.path.join(os.getcwd(), 'webapp/atom2rss.xsl'))
                xsltString = file.read()
                file.close()
                xsltSource = StreamSource(StringReader(xsltString))

                outputBuffer = StringWriter()

                transFactory = javax.xml.transform.TransformerFactory.newInstance("org.apache.xalan.processor.TransformerFactoryImpl",Thread.currentThread().getContextClassLoader())

                transformer = transFactory.newTransformer(xsltSource)
                transformer.transform(atomSource, StreamResult(outputBuffer))
                bs = outputBuffer.buffer.toString()
                header_str = 'text/xml;charset=utf-8'
            except MalformedURLException, mue:
                bs = "url format error"
            except TransformerException, te:
                bs = "transforme failed"
            except IOException, ie:
                bs = ie.getMessage()
            except Exception, e:
                bs = e.getMessage()
    else:
        bs = welcomeString

    res = bs.encode('utf-8')
    if header_str=='':
        header_str = 'text/html;charset=utf-8'

    start_response("200 Hoopy", [ ('content-type', header_str) ])
    return [res]
