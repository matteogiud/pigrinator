import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  //int _counter = 0;

  // void _incrementCounter() {
  //   setState(() {
  // This call to setState tells the Flutter framework that something has
  // changed in this State, which causes it to rerun the build method below
  // so that the display can reflect the updated values. If we changed
  // _counter without calling setState(), then the build method would not be
  // called again, and so nothing would appear to happen.
  //     _counter++;
  //   });
  // }

  var _items = [];
  String _error = "";
  //https://nominatim.openstreetmap.org/search?q=mariano+comense,+monnet&format=json&polygon_geojson=1&addressdetails=1
// http://pigrinatorstand.local/searchAllPaths
  void _getItems() async {
    // Make a WebSocket GET call here and retrieve the items
    // For example, using the http package:
    try {
      var json_response =
          "{ \"paths\": {\"1\": [{\"direction\": \"forward\", \"value\": 100}], \"2\": [{\"direction\": \"backward\", \"value\": 200}] }}";
      // var response = await http
      //     .get(Uri.parse('http://pigrinatorstand.local/searchAllPaths'));
      // if (response.statusCode == 200) {
      if (true) {
        //   var items = json
        //       .decode(response.body)
        //       .map((item) => item['paths'].toString())
        //       .toList();

        var items = json.decode(json_response);
        setState(() {
          _items = items;
          _selectedItem = null;
          _isItemSelected = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Connessione al robot avvenuta con successo!'),
          ),
        );
      } else {
        setState(() {
          _items = [];
          _selectedItem = null;
          _isItemSelected = false;
          _error = "Connection failed. Please try again later.";
          print(_error);
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(_error)),
        );
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
                'Connessione con il robot fallita! Controlla il WI-FI che stai utilizzando'),
          ),
        );
      }
    } on SocketException catch (_) {
      // Failure due to a network error
      setState(() {
        _items = [];
        _selectedItem = null;
        _isItemSelected = false;
        _error =
            "Could not connect to server. Please check your internet connection and try again.";
        print(_error);
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(_error)),
      );
    }
  }

  String? _selectedItem;
  bool _isItemSelected = false;

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      //body: Center(
      // Center is a layout widget. It takes a single child and positions it
      // in the middle of the parent.
      //child: Column(
      // Column is also a layout widget. It takes a list of children and
      // arranges them vertically. By default, it sizes itself to fit its
      // children horizontally, and tries to be as tall as its parent.
      //
      // Invoke "debug painting" (press "p" in the console, choose the
      // "Toggle Debug Paint" action from the Flutter Inspector in Android
      // Studio, or the "Toggle Debug Paint" command in Visual Studio Code)
      // to see the wireframe for each widget.
      //
      // Column has various properties to control how it sizes itself and
      // how it positions its children. Here we use mainAxisAlignment to
      // center the children vertically; the main axis here is the vertical
      // axis because Columns are vertical (the cross axis would be
      // horizontal).
      //       mainAxisAlignment: MainAxisAlignment.center,
      //       children: <Widget>[
      //         const Text(
      //           'You have pressed the button this many times:',
      //         ),
      //         Text(
      //           '$_counter',
      //           style: Theme.of(context).textTheme.headlineMedium,
      //         ),
      //       ],
      //     ),
      //   ),
      //   floatingActionButton: FloatingActionButton(
      //     onPressed: _incrementCounter,
      //     tooltip: 'Increment',
      //     child: const Icon(Icons.add),
      //   ), // This trailing comma makes auto-formatting nicer for build methods.
      // );

      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              if (_error.isNotEmpty)
                Text(
                  _error,
                  style: TextStyle(color: Colors.red),
                ),
              ElevatedButton(
                onPressed: _getItems,
                child: Text('Richiedi percorsi'),
              ),
              if (_items.isNotEmpty)
                DropdownButtonFormField(
                  value: _selectedItem,
                  items: _items.map((item) {
                    return DropdownMenuItem(
                      value: item,
                      child: Text(item),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      _selectedItem = value as String?;
                      _isItemSelected = true;
                    });
                    print(_selectedItem);
                  },
                  decoration: InputDecoration(
                    labelText: 'Select an item',
                    border: OutlineInputBorder(),
                  ),
                ),
              if (_isItemSelected)
                ElevatedButton(
                  onPressed: () {
                    print('Button pressed with $_selectedItem');
                    http.post(Uri.parse(
                        'http://pigrinatorstand.local/goTo$_selectedItem'));
                  },
                  child: const Text('VAI QUI!'),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
