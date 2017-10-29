import java.net.*;
import java.io.*;

class IOStreamTunnel extends Thread {
  private BufferedInputStream in;
  private BufferedOutputStream out;
  private String inname, outname, prefix;

  IOStreamTunnel(String pr, String iname, BufferedInputStream i, String oname, BufferedOutputStream o)
  {
    in = i;
    out = o;

    if(iname == null)
      inname = null;
    else
      inname = new String(iname);

    if(oname == null)
      outname = null;
    else
      outname = new String(oname);
    if(pr == null)
      prefix = null;
    else
      prefix = new String(pr);
  }

  private char toChar(int c) 
  {
    if( c < 10 || c > 126) return '#'; else return (char)c;
  }

  public void run() 
  {
    if( in == null || out == null || inname == null || outname == null ) return;

    int ch;	String str = prefix;

    try {
      while(true) {
        if(-1 != (ch = in.read())) {
          out.write(ch);
          out.flush();		  str = str + toChar(ch);
		  if (ch==10) { System.out.print(str); str = prefix; }
        }
      }
    }
    catch (IOException e) {
      System.out.println("IO Error in tunnel [" + inname +"->"+ outname +"]: " + e.getMessage());
      inname = null; outname = null;
      return;
    }
  }
}

class Sniffer 
{
  private Socket svSocket, clSocket;
  private BufferedInputStream clbis, svbis;
  private BufferedOutputStream clbos, svbos;

  public Sniffer() {
    svSocket = null;
    clSocket = null;
    svbis = null; svbos = null;
    clbis = null; clbos = null;
  }

  public Sniffer(String server, int svPort, int listenPort) {
    svSocket = null;
    clSocket = null;
    svbis = null; svbos = null;
    clbis = null; clbos = null;
    initConnections(server, svPort, listenPort);
  }

  public boolean bad() 
  {
    return
      svSocket == null || clSocket == null ||
      svbis == null || svbos == null || clbis == null || clbos == null;
  }

  public static void main(String argv[]) 
  {
    if(argv.length < 3) {
      System.out.println("usage: Sniffer <server> <serverport> <mylisten port>");
      return;
    }

    Sniffer me = new Sniffer(argv[0], Integer.parseInt(argv[1]), Integer.parseInt(argv[2]));

    if(me.bad())
      return;
    else
      me.startWork();

    return;
  }

  public boolean initConnections(String server, int svPort, int listenPort) 
  {
    try {
      ServerSocket tmpSocket = new ServerSocket(listenPort);
      System.out.println("Waiting for client connection on " + listenPort + "...");
      clSocket = tmpSocket.accept();
      tmpSocket.close();
      tmpSocket = null;
      System.out.println("Client connection accepted.");

      clbis = new BufferedInputStream(clSocket.getInputStream());
      clbos = new BufferedOutputStream(clSocket.getOutputStream());
    }
    catch (IOException e) {
      System.out.println("Could not accept client connection: " + e.getMessage());
      return false;
    }

    System.out.println("Connecting to server " + server + ":" + svPort + "...");
    try {
      svSocket = new Socket(server, svPort);
      svbis = new BufferedInputStream(svSocket.getInputStream());
      svbos = new BufferedOutputStream(svSocket.getOutputStream());
    }
    catch (IOException e) {
        svSocket = null;
        clSocket = null;
        clbis = null; clbos = null;
        System.out.println("Could not make server connection:" + e.getMessage());
        return false;
    }
    return true;
  }

  public void startWork() 
  {
	IOStreamTunnel clientToServer = new IOStreamTunnel("C: ", "client", clbis, "server", svbos);
	IOStreamTunnel serverToClient = new IOStreamTunnel("S: ", "server", svbis, "client", clbos);
    serverToClient.start();
    clientToServer.start();
  }
}

