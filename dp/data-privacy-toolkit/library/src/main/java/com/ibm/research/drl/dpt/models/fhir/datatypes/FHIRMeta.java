/*
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
*/
package com.ibm.research.drl.dpt.models.fhir.datatypes;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;

import java.util.Collection;

@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FHIRMeta {
    /* v1.0.2
    {
  // from Element: extension
  "versionId" : "<id>", // Version specific identifier
  "lastUpdated" : "<instant>", // When the resource version last changed
  "profile" : ["<uri>"], // Profiles this resource claims to conform to
  "security" : [{ Coding }], // Security Labels applied to this resource
  "tag" : [{ Coding }] // Tags applied to this resource
}
     */

    private String versionId;
    private String lastUpdated;
    private Collection<String> profile;
    private Collection<FHIRCoding> security;
    private Collection<FHIRCoding> tag;
}
