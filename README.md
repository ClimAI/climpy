# climpy

<center> <img src="climpy.png" alt="logo" style="width:100px;"/></center> 

Climpy is working to help climate researchers to analyse climate data, write in formats ready to be used with machine learning models and analyse the accuracy of model predictions

https://github.com/climai/climpy/actions/workflows/python-app.yml/badge.svg

The package is divided into three parts
- Transform: The `transform` module transforms by applying different conditions on your dataset. The class diagram below will detail on the application of the module.

```mermaid
---
Transform
---

classDiagram

Hazard <|-- Criterion

class Condition{
    args
    returns_event
    func()
}

class Criterion{
    sequence
    apply_conditions()
    valid_conditions(sequence) bool
}

class Hazard{

    event_locations
    n_events
    apply_conditions()
    valid_conditions()
    get_event(n) Event
    all_events() EventList
}

class DataArray{
    xr.DataArray variables
    xr.DataArray functions()
}

class LinkDataHazard{
    on_events()
    get_values()
}

class Event{
    data
    location
    start_time
    end_time
    
    r
    tau

    set_intensity()
}

class EventList{
    event_list
}

DataArray -- LinkDataHazard
LinkDataHazard -- Hazard
Hazard *-- EventList
EventList *--Event
Condition .. Criterion
Condition .. Hazard
```

- ml_data: The `ml_data` module creates/writes data to be used conveniently for different kinds of machine learning models. The class diagram below will detail on the application of the module.

```mermaid
---
Data ML
---
classDiagram


List *-- DataArray

class X{
    values
    meta
}

class Y{
    values
    meta
}

class MLData{
    X
    Y
    tvt_split()
}


class DataArray{
    xr.DataArray variables
    xr.DataArray functions()
}

class Split

```

- Metrics: The `metrics` module can be applied to observed and simulated variables. This would include exhaustive set of different metrics that can be used on climate related data