package com.web.fintrack.api;

import com.web.fintrack.domain.enums.TransactionCategory;
import com.web.fintrack.domain.enums.TransactionType;
import com.web.fintrack.domain.model.Record;
import com.web.fintrack.service.RecordService;
import javax.ws.rs.*;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.UriBuilder;

import java.net.URI;
import java.util.List;
import java.util.Optional;

@Path("/records")
@Produces("application/json")
public class RecordResource {

    private final RecordService recordService;

    public RecordResource() {
        this.recordService = new RecordService();
    }

    public RecordResource(RecordService recordService){
        this.recordService = recordService;
    }

    @POST
    @Consumes("application/json")
    @Produces("application/json")
    public Response create(Record record) {
        Record created = recordService.create(record);

        URI location = UriBuilder
                .fromResource(RecordResource.class)
                .path(created.getRecordId())
                .build();

        return Response
                .created(location)
                .entity(created)
                .build();
    }

    @GET
    @Path("/{id}")
    public Response findById(@PathParam("id") String id){
        Optional<Record> record = recordService.findById(new Record(null, 0, null, null, null, null, id));
        if(record.isPresent()) {
            return Response.ok(record.get()).build();
        }
        return Response.status(Response.Status.NOT_FOUND).build();
    }

    @GET
    @Path("/category/{category}")
    public Response findByCategory(@PathParam("category") TransactionCategory transactionCategory){
        List<Record> records = recordService.findByCategory(new Record(null, 0, transactionCategory, null, null, null, null));
        return Response.ok(records).build();
    }

    @GET
    @Path("/type/{type}")
    public Response findByType(@PathParam("type")TransactionType transactionType){
        List<Record> records = recordService.findByType(new Record(transactionType,0, null, null, null, null, null));
        return Response.ok(records).build();
    }

    @GET
    public List<Record> findAll(){
        return recordService.findAll();
    }

    @DELETE
    @Path("/{id}")
    public Response delete(@PathParam("id") String id) {
        recordService.deleteRecord(new Record(null, 0, null, null, null, null, id));
        return Response.noContent().build();
    }









}
